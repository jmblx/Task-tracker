import logging
import os
from typing import Any, Dict
from uuid import UUID

from fastapi import HTTPException
from jwt import ExpiredSignatureError, DecodeError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from strawberry import Info
import shutil
from PIL import Image

from auth.crud import get_user_by_token
from auth.utils import hash_password
from task.models import Task, Group
from auth.models import User
from database import async_session_maker, Base


async def create_upload_avatar(
    object_id,
    file,
    class_,
    path: str,
):
    async with async_session_maker() as session:
        object = await session.get(class_, object_id)
        save_path = os.path.join(path, f"object{object.id}{file.filename}")

        with open(save_path, "wb") as new_file:
            shutil.copyfileobj(file.file, new_file)

        with Image.open(save_path) as img:
            img = img.resize((350, 350))
            new_save_path = os.path.splitext(save_path)[0] + ".webp"
            img.save(new_save_path, "WEBP")

        # Удаляем старый файл
        os.remove(save_path)

        # Обновляем путь к файлу в объекте
        object.pathfile = new_save_path
        await session.commit()

    return new_save_path


async def get_object_images(
    class_: Any,
    object_ids: str,
):
    async with async_session_maker() as session:
        object_ids = object_ids.split(",")
        object_ids = list(map(lambda x: int(x), object_ids))
        images = {
            f"{(class_.__name__).lower()}{object_id}": (
                await session.get(class_, object_id)
            ).pathfile
            for object_id in object_ids
        }
        return images


def create_task_data(user: User, task: Task, group: Group):
    return {
        "first_name": user.first_name,
        "task_duration": task.duration,
        "task_name": task.name,
        "task_description": task.description,
        "task_start_time": task.added_at,
        "task_end_time": task.done_at,
        "task_group_name": group.name,
    }


async def prepare_data_mailing(user: User, task: Task, group: Group, redis) -> Dict:
    if await redis.smembers(f"auth:{user.tg_id}"):
        return {
            str(user.tg_id): create_task_data(
                user,
                task,
                group,
            )
        }
    return {}


async def insert_default(model_class: Base, data: dict):
    """
    Простой insert запрос в БД
    """
    async with async_session_maker() as session:
        model = model_class(**data)
        await session.add(model)
        await session.commit()
    return True


async def hash_user_pwd(session: AsyncSession, user_id: UUID, data: dict):
    user = await session.get(User, user_id)
    user.hashed_password = hash_password(data.get("password"))
    session.add(user)
    await session.commit()


async def validate_permission(info: Info, permission: str):
    try:
        token = info.context.get("auth_token").replace("Bearer ", "")
        print(token)
        user = await get_user_by_token(token)
    except (ExpiredSignatureError, DecodeError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    user_permissions = user.role.permissions
    if permission not in user_permissions:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)
