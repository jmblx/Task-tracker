from datetime import timedelta
from typing import Optional
from uuid import UUID

import strawberry
from fastapi_users.authentication.strategy import redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import user

from auth.models import User, Role
from auth.schemas import UserRead, RoleRead
from auth.task_read_schema import TaskRead
from database import async_session_maker
from gql_types import UserReadType, UserUpdateType, UserType, UserFindType, OrganizationFindType, OrganizationType, \
    OrganizationCreateType, \
    ProjectCreateType, ProjectFindType, ProjectType, OrganizationUpdateType, ProjectUpdateType, TaskFindType, TaskType, \
    TaskCreateType, TaskUpdateType, TaskReadType, GroupUpdateType, GroupCreateType, GroupFindType, GroupType, \
    RoleCreateType, RoleUpdateType, RoleFindType, RoleReadType
from organization.models import Organization
from project.models import Project
from project.schemas import ProjectRead
from task.group_schemas import GroupRead
from task.models import Task, Group

from utils import find_obj, insert_obj, update_object, insert_task, prepare_data_mailing, send_task_updates


@strawberry.type
class Query:
    @strawberry.field
    async def get_role(self, search_data: RoleFindType) -> Optional[RoleReadType]:
        validated_search_data = search_data.to_pydantic().dict(exclude_none=True)
        role = await find_obj(Role, validated_search_data)

        if role:
            role_data = RoleRead.from_orm(role)
            return RoleReadType.from_pydantic(role_data)
        else:
            return None

    @strawberry.field
    async def get_user(self, search_data: UserFindType) -> Optional[UserType]:
        validated_search_data = search_data.to_pydantic().dict(exclude_none=True)
        user = await find_obj(User, validated_search_data, [joinedload(User.role), joinedload(User.tasks)])

        if user:
            user_data = UserRead.from_orm(user)
            return UserType.from_pydantic(user_data)
        else:
            return None

    @strawberry.field
    async def get_organization(self, search_data: OrganizationFindType) -> Optional[OrganizationType]:
        validated_search_data = search_data.to_pydantic().dict(exclude_none=True)
        organization = await find_obj(
            Organization,
            validated_search_data,
            options=[
                joinedload(Organization.staff).joinedload(User.role),
                joinedload(Organization.projects).joinedload(Project.tasks)
            ]
        )
        if organization:
            workers = [user for user in organization.staff if user.role.name == "worker"]
            managers = [user for user in organization.staff if user.role.name == "manager"]
            print(organization.staff[0].role.name)
            return OrganizationType(
                id=str(organization.id),
                name=organization.name,
                description=organization.description,
                workers=[UserReadType.from_pydantic(user) for user in workers],
                managers=[UserReadType.from_pydantic(user) for user in managers],
                projects=[ProjectType.from_pydantic(project) for project in organization.projects],
            )
        else:
            return None

    @strawberry.field
    async def get_project(self, search_data: ProjectFindType) -> ProjectType:
        search_data = search_data.to_pydantic().model_dump()
        print(search_data)
        validated_search_data = {}
        for key, value in search_data.items():
            if value is not None:
                validated_search_data[key] = value
        data = await find_obj(
            Project, validated_search_data, [joinedload(Project.tasks), joinedload(Project.organization)]
        )
        data = ProjectRead.from_orm(data)
        data = ProjectType.from_pydantic(data)

        return data

    @strawberry.field
    async def get_task(self, search_data: TaskFindType) -> TaskReadType:
        search_data = search_data.to_pydantic().model_dump()
        validated_search_data = {k: v for k, v in search_data.items() if v is not None}

        async with async_session_maker() as session:
            query = select(Task).filter_by(**validated_search_data).options(
                joinedload(Task.assignees).joinedload(User.tasks),
                joinedload(Task.assigner).joinedload(User.tasks),
            )
            task_result = await session.execute(query)
            task = task_result.scalars().first()
            if task:
                print(task.__dict__)
                task_data = TaskRead.from_orm(task)
                result = TaskReadType.from_pydantic(task_data)
                return result
            else:
                raise ValueError("Задача не найдена")

    @strawberry.field
    async def get_group(self, search_data: GroupFindType) -> GroupType:
        async with async_session_maker() as session:
            query = select(Group).filter_by(**{k: v for k, v in search_data.__dict__.items() if v is not None})
            query = query.options(joinedload(Group.tasks), joinedload(Group.user).joinedload(User.role),
                                  joinedload(Group.user).joinedload(User.tasks))
            data = await session.execute(query)
            group = data.scalars().first()

        if group:
            group = GroupRead.from_orm(group)
            return GroupType.from_pydantic(group)
        else:
            raise LookupError("Group not found")


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def add_role(self, data: RoleCreateType) -> int:
        data = data.to_pydantic().model_dump()
        obj_id = await insert_obj(Role, data)
        return obj_id

    @strawberry.mutation
    async def update_role(self, item_id: int, data: RoleUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            Role,
            item_id
        )
        return True

    @strawberry.mutation
    async def update_user(self, id: strawberry.ID, data: UserUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            User,
            UUID(id)
        )
        return True

    @strawberry.mutation
    async def add_organization(self, data: OrganizationCreateType) -> int:
        search_data = data.to_pydantic().model_dump()
        obj_id = await insert_obj(Organization, search_data)
        return obj_id

    @strawberry.mutation
    async def update_organization(self, id: int, data: OrganizationUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            Organization,
            id
        )
        return True

    @strawberry.mutation
    async def add_project(self, data: ProjectCreateType) -> int:
        search_data = data.to_pydantic().model_dump()
        obj_id = await insert_obj(Project, search_data)
        return obj_id

    @strawberry.mutation
    async def update_project(self, id: int, data: ProjectUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            Project,
            id
        )
        return True

    @strawberry.mutation
    async def add_task(self, data: TaskCreateType) -> int:
        task_data = {
            'name': data.name,
            'description': data.description,
            'is_done': data.is_done,
            'assigner_id': data.assigner_id,
            'color': data.color,
            'duration': timedelta(seconds=data.duration),
            'difficulty': data.difficulty,
            'project_id': data.project_id,
            'group_id': data.group_id,
        }

        obj_id = await insert_task(
            Task, task_data, [assignee.__dict__ for assignee in data.assignees] if data.assignees else []
        )


        return obj_id

    @strawberry.mutation
    async def update_task(self, id: int, data: TaskUpdateType) -> bool:
        await update_object(data.to_pydantic(), Task, id)
        task = await Task.get(id=id)
        group = await Group.get(id=task.group_id)

        # Проверяем условия и отправляем уведомления
        data_mailing = await prepare_data_mailing(task.assigner, task, group, redis)
        if data_mailing:
            await send_task_updates(data_mailing)

        return True

    @strawberry.mutation
    async def decrease_task_time(self, id: int, seconds: int) -> bool:
        async with async_session_maker() as session:
            task = await session.get(Task, id)
            task.duration -= timedelta(seconds=seconds)
            await session.commit()
            return True

    @strawberry.mutation
    async def add_group(self, data: GroupCreateType) -> int:
        search_data = data.to_pydantic().model_dump()
        obj_id = await insert_obj(Group, search_data)
        return obj_id

    @strawberry.mutation
    async def update_group(self, id: int, data: GroupUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            Group,
            id
        )
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
