from typing import Union, List, Any, Callable, Tuple
from uuid import UUID

from fastapi import HTTPException
from slugify import slugify
from sqlalchemy import update, exc, select, insert, asc, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from strawberry import Info

from auth.jwt_utils import decode_jwt
from auth.models import User, Role
from db.database import async_session_maker, Base
from organization.models import Organization, UserOrg
from project.models import Project
from task.models import Task, Group, UserTask


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
                update(model).where(model.id == obj_id).values(update_data)
            )
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()


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
        if exc_fields is None:
            exc_fields = []
        entity_data = {
            key: value
            for key, value in data.items()
            if key not in exc_fields and value is not None
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


async def get_user_by_token(token: str) -> User:
    payload = decode_jwt(token)
    user = await get_user_by_id(payload.get("sub"), role=True)
    return user


async def get_user_by_id(user_id: UUID, role: bool = False) -> User:
    async with async_session_maker() as session:
        if role:
            query = (
                select(User).where(User.id == user_id).options(joinedload(User.role))
            )
            user = (await session.execute(query)).unique().scalar()
        else:
            user = await session.get(User, user_id)
        return user


async def delete_object(session: AsyncSession, obj_id: Union[int, UUID], model: Base):
    stmt = delete(model).where(model.id == obj_id)
    await session.execute(stmt)
    await session.commit()


async def soft_delete(session: AsyncSession, obj_id: Union[int, UUID], model: Base):
    stmt = update(model).where(model.id == obj_id).values(is_active=False)
    await session.execute(stmt)
    await session.commit()


# async def delete_organization(session: AsyncSession, obj_id: Union[int], info: Info):


async def full_delete_group(session: AsyncSession, obj_id: Union[int]):
    stmt = update(Task).where(Task.group_id == obj_id).values(group_id=None)
    await session.execute(stmt)
    await session.flush()
    await session.execute(delete(Group).where(Group.id == obj_id))
    await session.commit()


async def full_delete_user(session: AsyncSession, obj_id: Union[UUID]):
    orgs = (await session.execute(select(UserOrg).where(UserOrg.user_id == obj_id))).scalars().all()
    users_org = [org.id for org in orgs if "admin" in org.permissions]
    if users_org:
        raise HTTPException(
            status_code=403,
            detail=f"User is admin of orgs: {' '.join(map(str, users_org))}"
        )
    # await session.execute(delete(UserOrg).where(UserOrg.id.in_(users_org)))
    await session.execute(delete(UserTask).where(UserTask.user_id == obj_id))
    groups = (await (session.execute(select(Group).where(Group.user_id == obj_id)))).scalars().all()
    project_groups, user_groups = [], []
    for group in groups:
        if group.project_id is not None:
            project_groups.append(group.id)
        else:
            user_groups.append(group.id)
    await session.execute(delete(Group).where(Group.id.in_(user_groups)))
    await session.execute(update(Group).where(Group.id.in_(project_groups)).values(user_id=None))
    await session.execute(delete(User).where(User.id == obj_id))
    await session.commit()
