import json
import logging
import re
from datetime import timedelta
from functools import wraps
from inspect import signature
from typing import (
    Union,
    List,
    Any,
    Callable,
    Tuple,
    Dict,
    get_type_hints,
    Type,
    Optional,
)
from uuid import UUID

from fastapi import HTTPException
from nats.aio.client import Client as NATS
from aiokafka import AIOKafkaProducer
from faststream.nats import NatsBroker
from logstash import TCPLogstashHandler
from slugify import slugify
from sqlalchemy import update, exc, select, asc, desc, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    class_mapper,
    ColumnProperty,
    RelationshipProperty,
    joinedload,
    load_only,
)
from strawberry import Info
import secrets

import config
from auth.models import User, Role
from database import async_session_maker, Base
from organization.models import Organization
from project.models import Project
from task.models import Task, UserTask, Group
from utils import validate_permission

# logger = logging.getLogger("fastapi")
# logstash_handler = TCPLogstashHandler("logstash", 50000)


async def send_task_updates(data_mailing):
    producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        message = json.dumps(data_mailing).encode("utf-8")
        await producer.send_and_wait(config.PRODUCE_TOPIC, message)
    finally:
        await producer.stop()


async def update_object(
    data: dict,
    class_,
    obj_id: Union[int, UUID],
    query_options: List = None,
    if_slug: bool = False,
    attr_name: str = "name",
) -> Union[None, Any]:
    async with async_session_maker() as session:
        update_data = {key: value for key, value in data.items() if value is not None}
        if if_slug:
            update_data["slug"] = slugify(update_data.get(attr_name), lowercase=True)
        try:
            entity_id = (
                (
                    await session.execute(
                        update(class_)
                        .where(class_.id == obj_id)
                        .values(update_data)
                        .returning(class_.id)
                    )
                )
                .unique()
                .scalar()
            )
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
            update_data["slug"] = f'{update_data["slug"]}-{obj_id}'
            entity_id = await session.execute(
                update(class_)
                .where(class_.id == obj_id)
                .values(update_data)
                .returning(class_.id)
            )
            await session.commit()
        if query_options:
            query = select(class_)
            for option in query_options or []:
                query = query.options(option)
            entity = (
                (await session.execute(query.where(class_.id == entity_id)))
                .unique()
                .scalar()
            )
            return entity


async def default_update(model: Base, obj_id: Union[int, UUID], data: dict):
    print(obj_id)
    async with async_session_maker() as session:
        update_data = {key: value for key, value in data.items() if value is not None}
        try:
            await session.execute(
                update(model)
                .where(model.id == obj_id)
                .values(update_data)
            )
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()


def get_load_options(selected_fields):
    options = []
    if "role" in selected_fields:
        options.append(selectinload(User.role))
    if "tasks" in selected_fields:
        task_fields = selected_fields.get("tasks", {})
        task_options = [selectinload(User.tasks)]
        if "assignees" in task_fields:
            task_options.append(selectinload(Task.assignees))
        options.extend(task_options)
    return options


async def find_objs(class_, data: dict, options=None, order_by=None):
    async with async_session_maker() as session:
        query = select(class_)
        for key, value in data.items():
            if value is not None:
                query = query.where(getattr(class_, key) == value)

        if options:
            for option in options:
                query = query.options(option)

        if order_by:
            field = getattr(class_, order_by.field)
            direction = asc if order_by.direction.upper() == "ASC" else desc
            query = query.order_by(direction(field))

        result = (await session.execute(query)).unique().scalars().all()
        return result


def get_selected_fields(info, field_name):
    selected_fields = {}
    for field in info.selected_fields:
        if field.name == field_name:
            for sub_field in field.selections:
                selected_fields[sub_field.name] = get_selected_fields(
                    info, sub_field.name
                )
            break
    return selected_fields


async def insert_entity(
    model_class: Base,
    data: dict,
    query_options: List = None,
    process_extra: Callable = None,
    exc_fields: list = None,
) -> Tuple[Any, Union[int, UUID]]:
    """
    Формирующийся из запрошенных полей гибкий insert запрос, возвращающий объект с запрошенными данными
    """
    async with async_session_maker() as session:
        entity_data = {
            key: value for key, value in data.items() if key not in exc_fields
        }

        if hasattr(model_class, "id"):
            stmt = insert(model_class).values(entity_data).returning(model_class.id)
            result = await session.execute(stmt)
            entity_id = result.scalar()
        else:
            entity = model_class(**entity_data)
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            entity_id = entity.id

        if process_extra:
            await process_extra(session, entity_id, data)

        await session.commit()

        query = select(model_class)
        for option in query_options or []:
            query = query.options(option)
        entity = (
            (await session.execute(query.where(model_class.id == entity_id)))
            .unique()
            .scalar()
        )
        return entity, entity_id


async def process_task_assignees(
    session: AsyncSession, task_id: int, data: dict
) -> None:
    assignees = data.get("assignees", [])
    for assignee_data in assignees:
        assignee_data = to_snake_case(assignee_data)
        user = await session.get(User, assignee_data["id"])
        if user:
            is_employee = user.organization_id == assignee_data["organization_id"]
            user_task = UserTask(
                task_id=task_id,
                user_id=user.id,
                github_data=assignee_data.get("github_data"),
                is_employee=is_employee,
            )
            session.add(user_task)


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


def get_model(class_name: str):
    models = {
        "User": User,
        "Task": Task,
        "Organization": Organization,
        "Role": Role,
        "Group": Group,
        "Project": Project,
    }
    return models.get(class_name)


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


def add_from_instance(cls: Type):
    def from_instance(cls, instance, selected_fields: Dict = None):
        if selected_fields is None:
            selected_fields = {}
        kwargs = {}
        type_hints = get_type_hints(cls)

        for field, field_type in type_hints.items():
            if field in selected_fields:
                value = getattr(instance, field)

                if hasattr(field_type, "__origin__") and field_type.__origin__ == list:
                    element_type = field_type.__args__[0]
                    if hasattr(element_type, "from_instance"):
                        kwargs[field] = [
                            element_type.from_instance(v, selected_fields[field])
                            for v in value
                        ]
                    else:
                        kwargs[field] = value
                elif hasattr(field_type, "from_instance") and isinstance(
                    value, field_type
                ):
                    kwargs[field] = field_type.from_instance(
                        value, selected_fields[field]
                    )
                else:
                    kwargs[field] = value

        return cls(**kwargs)

    cls.from_instance = classmethod(from_instance)
    return cls


def strawberry_field_with_params(
    model_class: Base,
    result_type,
    search_field_name: str,
    need_validation: bool = True,
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            self, info: Info, search_data: dict, order_by: Optional[dict] = None
        ) -> List[Any]:
            if need_validation:
                await validate_permission(info, "read")
            operations = extract_selected_fields(info, search_field_name)
            normalized_operations = convert_dict_top_level_to_snake_case(operations)

            class_name = type(search_data).__name__
            model_name = extract_model_name(class_name)
            model = get_model(model_name)

            selected_fields = normalized_operations.get(f"get{model_name}", {})

            query_options = create_query_options(model, selected_fields)
            instances = await find_objs(
                model_class, search_data.__dict__, query_options, order_by
            )
            if instances:
                return [
                    result_type.from_instance(instance, selected_fields)
                    for instance in instances
                ]
            return []

        return wrapper

    return decorator


async def send_via_nats(nats_client: NATS, subject: str, json_message: str = None, data: dict = None, string: str = None):
    if json_message:
        await nats_client.publish(subject, json_message.encode('utf-8'))
    elif data:
        print(data)
        await nats_client.publish(subject, json.dumps(data).encode('utf-8'))
    elif string:
        await nats_client.publish(subject, string.encode('utf-8'))


def strawberry_insert_with_params(
    model_class: Base,
    process_extra: Optional[Callable] = None,
    exc_fields: list = None,
    notify_kwargs: Optional[Dict[str, str]] = None,
    notify_from_data_kwargs: Optional[Dict[str, str]] = None,
    notify_subject: Optional[str] = None,
    need_validation: bool = True,
    need_update: bool = True,
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, info: Info, data: dict, *args, **kwargs):
            if need_validation:
                await validate_permission(info, "insert")
            result_type = signature(func).return_annotation
            function_name = func.__name__
            selected_fields = extract_selected_fields(
                info, snake_to_camel(function_name)
            )
            normalized_operations = to_snake_case(selected_fields)
            selected_fields = normalized_operations.get(function_name, {})
            query_options = create_query_options(model_class, selected_fields)
            obj, obj_id = await insert_entity(
                model_class, data.__dict__, query_options, process_extra, exc_fields
            )
            if notify_from_data_kwargs is not None:
                notify_kwargs.update(
                    {k: data.__dict__[v] for k, v in notify_from_data_kwargs.items() if v in data.__dict__}
                )

                nats_client = info.context["nats_client"]
                await send_via_nats(
                    nats_client=nats_client,
                    subject=notify_subject,
                    data=notify_kwargs,
                )

                if need_update:
                    await default_update(model_class, obj_id, notify_kwargs)

            return result_type.from_instance(obj, selected_fields)

        return wrapper

    return decorator


async def decrease_task_time_by_id(id: int, seconds: int) -> bool:
    async with async_session_maker() as session:
        task = await session.get(Task, id)
        task.duration -= timedelta(seconds=seconds)
        await session.commit()
        return True


def strawberry_update_with_params(model_class: Base):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, info: Info, item_id: Union[int, UUID], data: Any):
            await validate_permission(info, "update")
            await update_object(data.__dict__, Role, item_id)
            result_type = signature(func).return_annotation
            function_name = func.__name__
            selected_fields = extract_selected_fields(
                info, snake_to_camel(function_name)
            )
            normalized_operations = to_snake_case(selected_fields)
            selected_fields = normalized_operations.get(function_name, {})

            query_options = create_query_options(model_class, selected_fields)
            obj = await update_object(
                data.__dict__, model_class, item_id, query_options
            )
            return result_type.from_instance(obj, selected_fields)

        return wrapper

    return decorator


async def find_user_by_search_data(find_data: dict) -> User:
    user = await find_objs(User, find_data, [load_only(User.id), load_only(User.email)])
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user[0]


async def send_request_change_password(user_email: str, nats_client: NATS) -> str:
    token: str = secrets.token_urlsafe(32)
    await send_via_nats(nats_client=nats_client, subject="email.reset_password", data={"token": token, "email": user_email})
    return token
