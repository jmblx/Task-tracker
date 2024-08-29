import logging
from collections.abc import Callable
from datetime import timedelta
from functools import wraps
from types import NoneType
from typing import Any, get_type_hints
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from strawberry import Info
from strawberry.scalars import JSON

from auth.jwt_utils import decode_jwt
from auth.models import User
from auth.validation import validate_permission
from db.database import Base
from db.utils import (
    delete_object,
    find_objs,
    insert_entity,
    soft_delete,
    update_object,
)
from deps.cont import container
from message_routing.nats_utils import process_notifications
from organization.models import UserOrg
from task.models import Task, UserTask
from utils import (
    GqlType,
    convert_dict_top_level_to_snake_case,
    create_query_options,
    extract_model_name,
    extract_selected_fields,
    get_func_data,
    snake_to_camel,
    to_snake_case,
)

logger = logging.getLogger("gql_utils")
# logstash_handler = TCPLogstashHandler("logstash", 50000)


async def process_task_assignees(
    session: AsyncSession, task_id: int, data: dict
) -> None:
    assignees = data.get("assignees", [])
    for assignee_data in assignees:
        assignee_data = to_snake_case(assignee_data.__dict__)
        user = (
            (
                await session.execute(
                    select(User)
                    .where(User.id == assignee_data["id"])
                    .options(selectinload(User.organizations))
                )
            )
            .unique()
            .scalar()
        )
        if user:
            org_id = assignee_data.get("organization_id")
            is_employee = (
                org_id
                in [organization.id for organization in user.organizations]
                if org_id and user.organizations
                else False
            )
            user_task = UserTask(
                task_id=task_id,
                user_id=user.id,
                github_data=assignee_data.get("github_data", None),
                is_employee=is_employee,
            )
            session.add(user_task)


async def process_project_staff(
    session: AsyncSession, org_id: int, data: dict
) -> None:
    staff = data.get("staff", [])
    for employee_data in staff:
        employee_data = to_snake_case(employee_data.__dict__)
        user_org = UserOrg(
            user_id=employee_data["id"],
            organization_id=org_id,
            position=employee_data["position"],
            permissions=employee_data["permissions"],
        )
        session.add(user_org)


def task_preprocess(data: dict, info: Info) -> dict:
    if "assigner_id" not in data:
        data["assigner_id"] = decode_jwt(
            info.context.user.id.access_token
        ).get("sub")
    return data


def add_from_instance(cls: type):
    def from_instance(cls, instance, selected_fields: dict | None = None):
        if selected_fields is None:
            selected_fields = {}
        kwargs = {}
        type_hints = get_type_hints(cls)

        for field, field_type in type_hints.items():
            if field in selected_fields:
                value = getattr(instance, field)

                if (
                    hasattr(field_type, "__origin__")
                    and field_type.__origin__ == list
                ):
                    element_type = field_type.__args__[0]
                    if hasattr(element_type, "from_instance"):
                        kwargs[field] = [
                            element_type.from_instance(
                                v, selected_fields[field]
                            )
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
    *,
    need_validation: bool = True,
):
    """
    Decorator to read object based on model,
     type_hints (return type and args types).
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            self,
            info: Info,
            search_data: dict,
            order_by: dict | None = None,
        ) -> list[Any]:
            if need_validation:
                await validate_permission(
                    info, model_class.__tablename__, "read"
                )

            # async with container() as di:
            #     session = await di.get(AsyncSession)
            operations = extract_selected_fields(info, search_field_name)
            normalized_operations = convert_dict_top_level_to_snake_case(
                operations
            )
            class_name = type(search_data).__name__
            model_name = extract_model_name(class_name)
            selected_fields = normalized_operations.get(f"get{model_name}", {})
            query_options = create_query_options(model_class, selected_fields)

            instances = await find_objs(
                model_class,
                search_data.__dict__,
                query_options,
                order_by,
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
    session: AsyncSession,
    function_name: str,
    data_process_extra: Callable[[dict, Info], dict] | None = None,
    process_extra_db: Callable[[AsyncSession, dict], Any] | None = None,
    exc_fields: list[str] | None = None,
) -> tuple:
    selected_fields = extract_selected_fields(
        info, snake_to_camel(function_name)
    )
    normalized_operations = to_snake_case(selected_fields)
    selected_fields = normalized_operations.get(function_name, {})
    query_options = create_query_options(model_class, selected_fields)

    data = data if isinstance(data, dict) else data.__dict__
    data = data_process_extra(data, info) if data_process_extra else data
    obj, obj_id = await insert_entity(
        model_class, data, session, query_options, process_extra_db, exc_fields
    )

    return obj, obj_id, selected_fields


def strawberry_insert(
    model_class: Base,
    data_process_extra: Callable[[dict, Info], dict] | None = None,
    process_extra_db: (
        Callable[[AsyncSession, int | UUID, dict], Any] | None
    ) = None,
    exc_fields: list[str] | None = None,
    notify_kwargs: dict[str, str] | None = None,
    notify_from_data_kwargs: dict[str, str] | None = None,
    notify_subject: str | None = None,
    validation: bool = True,  # noqa: FBT001, FBT002
    need_update: bool = True,  # noqa: FBT001, FBT002
) -> Callable[[Callable], Callable]:
    """
    Decorator to insert object based on model,
    type_hints (return type and args types).
    With notify_kwargs can be used to send notifications.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, info: Info, data: dict) -> Any:

            if validation:
                await validate_permission(
                    info, model_class.__tablename__, "create"
                )

            function_name, result_type = get_func_data(func)

            async with container() as di:
                session = await di.get(AsyncSession)

            obj, obj_id, selected_fields = await process_data_and_insert(
                info,
                model_class,
                data,
                session,
                function_name,
                data_process_extra,
                process_extra_db,
                exc_fields,
            )

            if notify_subject:
                await process_notifications(
                    data,
                    notify_from_data_kwargs,
                    notify_kwargs,
                    notify_subject,
                    model_class,
                    obj_id,
                    need_update=need_update,
                )

            return result_type.from_instance(obj, selected_fields)

        return wrapper

    return decorator


async def decrease_task_time_by_id(task_id: int, seconds: int) -> bool:
    async with container() as di:
        session = await di.get(AsyncSession)
        task = await session.get(Task, task_id)
        task.duration -= timedelta(seconds=seconds)
        await session.commit()
    return True


def strawberry_update(
    model_class: type[Base],
) -> Callable[[Callable], Callable]:
    """
    decorator to update object based on model,
    type_hints (return type and args types)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            self, info: Info, item_id: int | UUID, data: Any
        ) -> GqlType | dict | None:
            await validate_permission(
                info, model_class.__tablename__, "update"
            )

            function_name, result_type = get_func_data(func)
            async with container() as di:
                session = await di.get(AsyncSession)

                if result_type in [NoneType, JSON]:
                    await update_object(
                        data.__dict__, model_class, item_id, session
                    )
                    return {"status": "ok"}

                selected_fields = extract_selected_fields(
                    info, snake_to_camel(function_name)
                )
                normalized_operations: dict = to_snake_case(selected_fields)
                selected_fields = normalized_operations.get(function_name, {})

                query_options = create_query_options(
                    model_class, selected_fields
                )
                obj = await update_object(
                    data.__dict__, model_class, item_id, session, query_options
                )
                return result_type.from_instance(obj, selected_fields)

        return wrapper

    return decorator


def strawberry_delete(
    model_class: Base,
    full_delete_param: bool | None = None,
    del_func: Callable[[AsyncSession, int | UUID], Any] | None = None,
):
    """
    decorator to delete object based on model,
     type_hints (return type and args types)
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, item_id: int | UUID, info: Info):
            await validate_permission(
                info, model_class.__tablename__, "delete"
            )

            full_delete = (
                full_delete_param
                if full_delete_param is not None
                else "is_active"
                not in model_class.__dict__.get("__annotations__", {})
            )

            async with container() as di:
                session = await di.get(AsyncSession)

                delete_function = del_func
                if delete_function is None:
                    delete_function = (
                        delete_object if full_delete else soft_delete
                    )

                await delete_function(session, item_id, model_class)

                function_name, result_type = get_func_data(func)
                if result_type in [NoneType, JSON]:
                    return {"status": "successfully deleted"}

                selected_fields = extract_selected_fields(
                    info, snake_to_camel(function_name)
                )
                normalized_operations = to_snake_case(selected_fields)
                selected_fields = normalized_operations.get(function_name, {})

                query_options = create_query_options(
                    model_class, selected_fields
                )
                instances = await find_objs(
                    model_class, {"id": item_id}, session, query_options
                )

            if not instances:
                raise HTTPException(status_code=404)

            return result_type.from_instance(instances[0], selected_fields)

        return wrapper

    return decorator
