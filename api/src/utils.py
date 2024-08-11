import inspect
import os
import re
from typing import Any, Dict, Callable, Type, Tuple, List, Union, get_type_hints
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
import shutil
from PIL import Image
from sqlalchemy.orm import (
    class_mapper,
    ColumnProperty,
    RelationshipProperty,
    selectinload,
    joinedload,
    load_only,
)

from auth.jwt_utils import hash_password
from task.models import Task, Group
from auth.models import User
from db.database import async_session_maker, Base


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


def get_func_data(func: Callable) -> tuple[str, Type]:
    function_name = func.__name__

    signature = inspect.signature(func)
    return_annotation = signature.return_annotation

    return function_name, return_annotation


def extract_selected_fields(info, field_name):
    selected_fields = {}

    for field in info.selected_fields:
        if field.name == field_name:
            selected_fields[field.name] = process_selections(field.selections)
            break

    return selected_fields


def process_selections(selections):
    fields = {}

    for selection in selections:
        if selection.selections:
            fields[selection.name] = process_selections(selection.selections)
        else:
            fields[selection.name] = {}

    return fields


def get_model_fields(model: Any) -> Tuple[List[str], Dict[str, Any]]:
    """Возвращает кортеж из двух списков: физических полей и полей отношений."""
    mapper = class_mapper(model)
    physical_fields = []
    relationship_fields = {}

    for prop in mapper.iterate_properties:
        if isinstance(prop, ColumnProperty):
            physical_fields.append(prop.key)
        elif isinstance(prop, RelationshipProperty):
            relationship_fields[prop.key] = prop.mapper.class_

    return physical_fields, relationship_fields


def extract_model_name(class_name: str) -> Base:
    match = re.match(r"^[A-Z][a-z]*[A-Z]", class_name)
    if match:
        return match.group(0)[:-1]
    return class_name


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.capitalize() for x in components[1:])


def camel_to_snake(name):
    """Преобразует camelCase в snake_case"""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_snake_case(data, keep_top_level_keys=False) -> Union[dict, list]:
    """Преобразует ключи словаря и его вложенных словарей в snake_case"""
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = key if keep_top_level_keys else camel_to_snake(key)
            new_dict[new_key] = to_snake_case(value)
        return new_dict
    elif isinstance(data, list):
        return [to_snake_case(item) for item in data]
    else:
        return data


def convert_dict_top_level_to_snake_case(data):
    """Преобразует только вложенные ключи в snake_case, ключи первого уровня оставляет неизменными"""
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_dict[key] = to_snake_case(value, keep_top_level_keys=False)
        return new_dict
    else:
        return data


def create_query_options(model: Any, fields: Dict[str, Any]) -> List:
    """Рекурсивно создает опции запроса для загрузки нужных полей и вложенных отношений."""
    physical_fields, relationship_fields = get_model_fields(model)
    options = []

    for field, subfields in fields.items():
        if field in relationship_fields:
            rel_model = relationship_fields[field]
            field_type = get_type_hints(model).get(field, None)
            if (
                field_type
                and hasattr(field_type, "__origin__")
                and field_type.__origin__ == list
            ):
                sub_options = create_query_options(rel_model, subfields)
                options.append(
                    selectinload(getattr(model, field)).options(*sub_options)
                )
            else:
                sub_options = create_query_options(rel_model, subfields)
                options.append(joinedload(getattr(model, field)).options(*sub_options))

        elif field in physical_fields:
            options.append(load_only(getattr(model, field)))

    return options
