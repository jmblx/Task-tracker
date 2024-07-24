from typing import Optional, List

import strawberry
from strawberry import Info

from auth.models import User, Role
from gql_types import UserType, UserFindType, RoleType, RoleFindType, OrganizationType, \
    OrganizationFindType, ProjectType, ProjectFindType, TaskType, TaskFindType, GroupType, GroupFindType, OrderByInput
from organization.models import Organization
from project.models import Project
from task.models import Task, Group
from utils import strawberry_field_with_params


@strawberry.type
class Query:

    @strawberry.field
    @strawberry_field_with_params(Role, RoleType, 'getRole')
    async def get_role(self, info: Info, search_data: RoleFindType, order_by: Optional[OrderByInput] = None) -> Optional[List[RoleType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(User, UserType, 'getUser')
    async def get_user(self, info: Info, search_data: UserFindType, order_by: Optional[OrderByInput] = None) -> Optional[List[UserType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Task, TaskType, 'getTask')
    async def get_task(self, info: Info, search_data: TaskFindType, order_by: Optional[OrderByInput] = None) -> Optional[List[TaskType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Organization, OrganizationType, 'getOrganization')
    async def get_organization(self, info: Info, search_data: OrganizationFindType, order_by: Optional[OrderByInput] = None) -> Optional[List[OrganizationType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Project, ProjectType, 'getProject')
    async def get_project(self, info: Info, search_data: ProjectFindType, order_by: Optional[OrderByInput] = None) -> Optional[List[ProjectType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Group, GroupType, 'getGroup')
    async def get_group(self, info: Info, search_data: GroupFindType, order_by: Optional[OrderByInput] = None) -> Optional[List[GroupType]]:
        pass
