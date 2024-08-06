import re
from datetime import timedelta
from functools import wraps
import inspect
from typing import (
    Union,
    List,
    Any,
    Callable,
    Tuple,
    Dict,
    get_type_hints,
    Type,
    Optional, )
from uuid import UUID

from fastapi import HTTPException
from jwt import ExpiredSignatureError, DecodeError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    class_mapper,
    ColumnProperty,
    RelationshipProperty,
    joinedload,
    load_only,
)
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from strawberry import Info

from auth.models import User, Role
from db.database import async_session_maker, Base
from db.utils import update_object, insert_entity, find_objs, get_model, get_user_by_token, delete_object, soft_delete
from message_routing.nats_utils import process_notifications
from task.models import Task, UserTask


# logger = logging.getLogger("fastapi")
# logstash_handler = TCPLogstashHandler("logstash", 50000)


async def process_task_assignees(
    session: AsyncSession, task_id: int, data: dict
) -> None:
    assignees = data.get("assignees", [])
    for assignee_data in assignees:
        assignee_data = to_snake_case(assignee_data)
        user = await session.get(User, assignee_data["id"])
        if user:
            is_employee = user.organization_id == assignee_data.get("organization_id", False)
            user_task = UserTask(
                task_id=task_id,
                user_id=user.id,
                github_data=assignee_data.get("github_data", None),
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


def strawberry_read(
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
                await validate_permission(info, model_class.__tablename__, "read")
            operations = extract_selected_fields(info, search_field_name)
            normalized_operations = convert_dict_top_level_to_snake_case(operations)

            class_name = type(search_data).__name__
            model_name = extract_model_name(class_name)

            selected_fields = normalized_operations.get(f"get{model_name}", {})

            query_options = create_query_options(model_class, selected_fields)
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


async def process_data_and_insert(
    info: Info,
    model_class: Base,
    data: Any,
    function_name: str,
    data_process_extra: Optional[Callable[[dict], dict]] = None,
    process_extra_db: Optional[Callable[[Any], Any]] = None,
    exc_fields: Optional[List[str]] = None
) -> tuple:
    selected_fields = extract_selected_fields(info, snake_to_camel(function_name))
    normalized_operations = to_snake_case(selected_fields)
    selected_fields = normalized_operations.get(function_name, {})
    query_options = create_query_options(model_class, selected_fields)
    data = data_process_extra(data) if data_process_extra else data
    data = data if isinstance(data, dict) else data.__dict__
    obj, obj_id = await insert_entity(
        model_class, data, query_options, process_extra_db, exc_fields
    )
    return obj, obj_id, selected_fields


def get_func_data(func: Callable) -> tuple[str, Type]:
    function_name = func.__name__

    signature = inspect.signature(func)
    return_annotation = signature.return_annotation

    return function_name, return_annotation


def strawberry_insert(
    model_class: Base,
    data_process_extra: Optional[Callable[[dict], dict]] = None,
    process_extra_db: Optional[Callable[[Any], Any]] = None,
    exc_fields: List[str] = None,
    notify_kwargs: Optional[Dict[str, str]] = None,
    notify_from_data_kwargs: Optional[Dict[str, str]] = None,
    notify_subject: Optional[str] = None,
    need_validation: bool = True,
    need_update: bool = True,
) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, info: Info, data: dict) -> Any:
            if need_validation:
                await validate_permission(info, model_class.__tablename__, "insert")
            function_name, result_type = get_func_data(func)

            obj, obj_id, selected_fields = await process_data_and_insert(
                info, model_class, data, function_name, data_process_extra, process_extra_db, exc_fields
            )

            await process_notifications(
                info, data, notify_from_data_kwargs, notify_kwargs, notify_subject, model_class, obj_id, need_update
            )

            return result_type.from_instance(obj, selected_fields)

        return wrapper

    return decorator


async def decrease_task_time_by_id(id: int, seconds: int) -> bool:
    async with async_session_maker() as session:
        task = await session.get(Task, id)
        task.duration -= timedelta(seconds=seconds)
        await session.commit()
        return True


def strawberry_update(model_class: Base):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, info: Info, item_id: Union[int, UUID], data: Any):
            await validate_permission(info, model_class.__tablename__, "update")
            await update_object(data.__dict__, Role, item_id)
            function_name, result_type = get_func_data(func)
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


async def validate_permission(info: Info, entity: str, permission: str):
    try:
        token = info.context.get("auth_token").replace("Bearer ", "")
        print(token)
        user = await get_user_by_token(token)
    except (ExpiredSignatureError, DecodeError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    entity_permissions = user.role.permissions.get(entity)
    if permission not in entity_permissions:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)


def strawberry_delete(model_class: Base, full_delete: bool):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, info: Info, item_id: Union[int, UUID]):
            await validate_permission(info, model_class.__tablename__, "delete")
            function_name, result_type = get_func_data(func)
            selected_fields = extract_selected_fields(
                info, snake_to_camel(function_name)
            )
            normalized_operations = to_snake_case(selected_fields)
            selected_fields = normalized_operations.get(function_name, {})

            query_options = create_query_options(model_class, selected_fields)
            instances = await find_objs(
                model_class, {"id": item_id}, query_options
            )
            async with async_session_maker() as session:
                if full_delete:
                    await delete_object(session, item_id, model_class)
                else:
                    await soft_delete(session, item_id, model_class)
            if instances:
                return [
                    result_type.from_instance(instance, selected_fields)
                    for instance in instances
                ]
            return []

        return wrapper

    return decorator
