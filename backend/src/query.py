from typing import Optional
import re

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import selectinload, load_only
from strawberry import Info

from auth.models import User, Role
from organization.models import Organization
from project.models import Project
from task.models import Task, Group
from gql_types import UserType, UserFindType, RoleType, RoleFindType, OrganizationType, \
    OrganizationFindType, ProjectType, ProjectFindType, TaskType, TaskFindType, GroupType, GroupFindType
from utils import find_obj, get_selected_fields, extract_selected_fields, extract_model_name, \
    get_model, get_model_fields, convert_dict_top_level_to_snake_case, create_query_options, \
    strawberry_field_with_params


@strawberry.type
class Query:

    @strawberry.field
    @strawberry_field_with_params(Role, RoleType, 'getRole')
    async def get_role(self, info: Info, search_data: RoleFindType) -> Optional[RoleType]:
        pass

    @strawberry.field
    @strawberry_field_with_params(User, UserType, 'getUser')
    async def get_user(self, info: Info, search_data: UserFindType) -> Optional[UserType]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Task, TaskType, 'getTask')
    async def get_task(self, info: Info, search_data: TaskFindType) -> Optional[TaskType]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Organization, OrganizationType, 'getOrganization')
    async def get_organization(self, info: Info, search_data: OrganizationFindType) -> Optional[OrganizationType]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Project, ProjectType, 'getProject')
    async def get_project(self, info: Info, search_data: ProjectFindType) -> Optional[ProjectType]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Group, GroupType, 'getGroup')
    async def get_group(self, info: Info, search_data: GroupFindType) -> Optional[GroupType]:
        pass
