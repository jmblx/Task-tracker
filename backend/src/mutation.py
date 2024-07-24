import inspect
from uuid import UUID

import strawberry
from strawberry import Info

from auth.models import User, Role
from organization.models import Organization
from project.models import Project
from task.models import Task, Group
from gql_types import UserCreateType, UserUpdateType, RoleCreateType, RoleUpdateType, OrganizationCreateType, \
    OrganizationUpdateType, ProjectCreateType, ProjectUpdateType, TaskCreateType, TaskUpdateType, GroupUpdateType, \
    GroupCreateType, RoleType, OrganizationType, ProjectType, TaskType, GroupType, UserType
from utils import update_object, \
    decrease_task_time_by_id, strawberry_mutation_with_params, process_task_assignees, strawberry_update_with_params


@strawberry.type
class Mutation:
    @strawberry.mutation
    @strawberry_mutation_with_params(Role)
    async def add_role(self, info: Info, data: RoleCreateType) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_update_with_params(Role)
    async def update_role(self, info: Info, item_id: int, data: RoleUpdateType) -> RoleType:
        # await update_object(data.__dict__, Role, item_id)
        pass

    @strawberry.mutation
    @strawberry_update_with_params(User)
    async def update_user(self, info: Info, item_id: UUID, data: UserUpdateType) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_mutation_with_params(Organization)
    async def add_organization(self, info: Info, data: OrganizationCreateType) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_update_with_params(Organization)
    async def update_organization(self, info: Info, item_id: int, data: OrganizationUpdateType) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_mutation_with_params(Project)
    async def add_project(self, info: Info, data: ProjectCreateType) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_update_with_params(Project)
    async def update_project(self, info: Info, item_id: int, data: ProjectUpdateType) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_mutation_with_params(Task, process_task_assignees)
    async def add_task(self, info: Info, data: TaskCreateType) -> TaskType:
        pass

    @strawberry.mutation
    @strawberry_update_with_params(Task)
    async def update_task(self, info: Info, item_id: int, data: TaskUpdateType) -> TaskType:
        pass

    @strawberry.mutation
    async def decrease_task_time(self, item_id: int, seconds: int) -> bool:
        await decrease_task_time_by_id(item_id, seconds)
        return True

    @strawberry.mutation
    @strawberry_mutation_with_params(Group)
    async def add_group(self, info: Info, data: GroupCreateType) -> GroupType:
        pass

    @strawberry.mutation
    @strawberry_update_with_params(Group)
    async def update_group(self, info: Info, item_id: int, data: GroupUpdateType) -> GroupType:
        pass
