from fastapi.templating import Jinja2Templates

import config
from task.models import UserTask, Task, Group

templates = Jinja2Templates(directory="templates")

import os
from aiokafka import AIOKafkaProducer
import json
from typing import Any, Dict, List

from pydantic import BaseModel
from slugify import slugify
from sqlalchemy import select, text, or_, func, update, exc, and_, insert
import shutil
from PIL import Image

from auth.models import User
from database import async_session_maker


# Базовая функция для сбора данных с БД
async def get_data(class_, filter, is_scalar: bool = False, order_by=None):
    async with async_session_maker() as session:
        stmt = select(class_).where(filter)
        if is_scalar:
            res_query = await session.execute(stmt)
            res = res_query.scalar()
        else:
            if order_by:
                stmt = select(class_).where(filter).order_by(order_by)
            res_query = await session.execute(stmt)
            res = res_query.fetchall()
            res = [result[0] for result in res]
    return res


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


def create_task_data(
    user: User, task: Task, group: Group
):
    return {
        "first_name": user.first_name,
        "task_duration": task.duration,
        "task_name": task.name,
        "task_description": task.description,
        "task_start_time": task.added_at,
        "task_end_time": task.done_at,
        "task_group_name": group.name,
    }


async def prepare_data_mailing(
    user: User, task: Task, group: Group, redis
) -> Dict:
    if await redis.smembers(f"auth:{user.tg_id}"):
        return {
            str(user.tg_id): create_task_data(
                user, task, group,
            )
        }
    return {}


async def send_task_updates(data_mailing):
    producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        message = json.dumps(data_mailing).encode('utf-8')
        await producer.send_and_wait(config.PRODUCE_TOPIC, message)
    finally:
        await producer.stop()


async def update_object(
    data: BaseModel,
    class_,
    obj_id: int,
    if_slug: bool = False,
    attr_name: str = "name",
) -> None:
    async with async_session_maker() as session:
        update_data = {
            key: value
            for key, value in data.model_dump().items()
            if value is not None
        }
        if if_slug:
            update_data["slug"] = slugify(
                update_data.get(attr_name), lowercase=True
            )
        try:
            await session.execute(
                update(class_).where(class_.id == obj_id).values(update_data)
            )
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
            update_data["slug"] = f'{update_data["slug"]}-{obj_id}'
            await session.execute(
                update(class_).where(class_.id == obj_id).values(update_data)
            )
            await session.commit()


async def find_obj(class_, data: dict, options=None):
    async with async_session_maker() as session:
        query = select(class_).filter_by(**data)
        if options:
            for option in options:
                query = query.options(option)
        result = (await session.execute(query)).scalars().first()
        return result


async def insert_obj(class_, data: dict) -> int:
    async with async_session_maker() as session:
        query = insert(class_).values(data).returning(class_.id)
        result = (await session.execute(query)).scalar()
        await session.commit()
        return result


async def insert_task(class_, data: dict, assignees_data: List[Dict[str, Any]]) -> int:
    async with async_session_maker() as session:
        query = insert(class_).values(data).returning(class_.id)
        result = await session.execute(query)
        task_id = result.scalar()

        for assignee_data in assignees_data:
            user = await session.get(User, assignee_data['id'])
            if user:
                print(data)
                is_employee = user.organization_id == assignee_data['organization_id']
                user_task = UserTask(
                    task_id=task_id,
                    user_id=user.id,
                    github_data=assignee_data.get('github_data'),
                    is_employee=is_employee
                )
                session.add(user_task)

        await session.commit()
        return task_id

