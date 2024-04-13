from uuid import UUID

import strawberry

from auth.models import User
from auth.schemas import UserRead
from gql_types import UserReadType, UserUpdateType, UserType, UserFindType, OrganizationFindType, OrganizationType, OrganizationCreateType, \
    ProjectCreateType, ProjectFindType, ProjectType, OrganizationUpdateType, ProjectUpdateType, TaskFindType, TaskType, \
    TaskCreateType, TaskUpdateType
from organization.models import Organization
from organization.schemas import OrganizationRead
from project.models import Project
from project.schemas import ProjectRead
from task.models import Task
from task.schemas import TaskRead
from utils import find_obj, insert_obj, update_object


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, search_data: UserFindType) -> UserType:
        search_data = search_data.to_pydantic().model_dump()
        print(search_data)
        validated_search_data = {}
        for key, value in search_data.items():
            if value is not None:
                validated_search_data[key] = value
        data = await find_obj(User, validated_search_data)
        data = UserRead.from_orm(data)
        return data

    @strawberry.field
    async def get_organization(self, search_data: OrganizationFindType) -> OrganizationType:
        search_data = search_data.to_pydantic().model_dump()
        print(search_data)
        validated_search_data = {}
        for key, value in search_data.items():
            if value is not None:
                validated_search_data[key] = value
        data = await find_obj(Organization, validated_search_data)
        data = OrganizationRead.from_orm(data)
        return data

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
    async def get_task(self, search_data: TaskFindType) -> TaskType:
        search_data = search_data.to_pydantic().model_dump()
        print(search_data)
        validated_search_data = {}
        for key, value in search_data.items():
            if value is not None:
                validated_search_data[key] = value
        data = await find_obj(Task, validated_search_data)
        data = TaskRead.from_orm(data)
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
        search_data = data.to_pydantic().model_dump()
        obj_id = await insert_obj(Task, search_data)
        return obj_id

    @strawberry.mutation
    async def update_task(self, id: int, data: TaskUpdateType) -> bool:
        await update_object(
            data.to_pydantic(),
            Task,
            id
        )
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
