from datetime import timedelta
from typing import Optional
from uuid import UUID

import strawberry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm import joinedload


from auth.models import User
from auth.schemas import UserRead
from auth.task_read_schema import TaskRead
from database import async_session_maker
from gql_types import UserReadType, UserUpdateType, UserType, UserFindType, OrganizationFindType, OrganizationType, \
    OrganizationCreateType, \
    ProjectCreateType, ProjectFindType, ProjectType, OrganizationUpdateType, ProjectUpdateType, TaskFindType, TaskType, \
    TaskCreateType, TaskUpdateType, TaskReadType
from organization.models import Organization
from project.models import Project
from project.schemas import ProjectRead
from task.models import Task

from utils import find_obj, insert_obj, update_object, insert_task


@strawberry.type
class Query:

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
                joinedload(Organization.staff).joinedload(User.role)
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
                managers=[UserReadType.from_pydantic(user) for user in managers]
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
        data = await find_obj(Project, validated_search_data)
        data = ProjectRead.from_orm(data)
        return data

    @strawberry.field
    async def get_task(self, search_data: TaskFindType) -> TaskReadType:
        search_data = search_data.to_pydantic().model_dump()
        validated_search_data = {k: v for k, v in search_data.items() if v is not None}
        data = await find_obj(Task, validated_search_data, [
            joinedload(Task.assignees).joinedload(User.role),
        ])
        async with async_session_maker() as session:
            data.assigner = (await session.execute(select(User).where(User.id == data.assigner_id).options(joinedload(User.role)))).unique().scalar()
            data = TaskRead.from_orm(data)
            data = TaskReadType.from_pydantic(data)
            return data


@strawberry.type
class Mutation:

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
        # Теперь `data` напрямую содержит нужные поля, которые можно использовать
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

        obj_id = await insert_task(Task, task_data, [assignee.__dict__ for assignee in data.assignees] if data.assignees else [])

        return obj_id

    @strawberry.mutation
    async def update_task(self, id: int, data: TaskUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            Task,
            id
        )
        return True

    @strawberry.mutation
    async def decrease_task_time(self, id: int, seconds: int) -> bool:
        async with async_session_maker() as session:
            task = await session.get(Task, id)
            task.duration -= timedelta(seconds=seconds)
            await session.commit()
            return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
