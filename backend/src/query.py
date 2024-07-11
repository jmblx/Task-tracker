from typing import Optional

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from strawberry import Info

from auth.models import User, Role
from organization.models import Organization
from project.models import Project
from task.models import Task, Group
from gql_types import UserType, UserFindType, RoleType, RoleFindType, OrganizationType, \
    OrganizationFindType, ProjectType, ProjectFindType, TaskType, TaskFindType, GroupType, GroupFindType
from utils import find_obj, get_selected_fields


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: Info, search_data: UserFindType) -> Optional[UserType]:
        selected_fields = get_selected_fields(info, 'getUser')
        user = await find_obj(
            User,
            search_data.__dict__,
            selected_fields
        )
        if user:
            return UserType.from_instance(user, selected_fields)
        return None

    @strawberry.field
    async def get_task(self, info: Info, search_data: TaskFindType) -> Optional[TaskType]:
        selected_fields = get_selected_fields(info, 'get_task')
        task = await find_obj(Task, search_data.__dict__, selected_fields)
        if task:
            return TaskType.from_instance(task)
        return None

    @strawberry.field
    async def get_organization(self, info: Info, search_data: OrganizationFindType) -> Optional[OrganizationType]:
        selected_fields = get_selected_fields(info, 'get_organization')
        organization = await find_obj(Organization, search_data.__dict__, selected_fields)
        if organization:
            return OrganizationType.from_instance(organization)
        return None

    @strawberry.field
    async def get_project(self, info: Info, search_data: ProjectFindType) -> Optional[ProjectType]:
        selected_fields = get_selected_fields(info, 'get_project')
        project = await find_obj(Project, search_data.__dict__, selected_fields)
        if project:
            return ProjectType.from_instance(project)
        return None

    @strawberry.field
    async def get_group(self, info: Info, search_data: GroupFindType) -> Optional[GroupType]:
        selected_fields = get_selected_fields(info, 'get_group')
        group = await find_obj(Group, search_data.__dict__, selected_fields)
        if group:
            return GroupType.from_instance(group)
        return None



