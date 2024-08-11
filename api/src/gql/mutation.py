from uuid import UUID

import strawberry
from strawberry import Info
import secrets

from auth.models import User, Role
from auth.reset_pwd_utils import set_new_pwd
from config import GOOGLE_OAUTH_CLIENT_ID
from myredis.redis_config import get_redis
from myredis.utils import get_user_id_from_reset_pwd_token
from organization.models import Organization
from project.models import Project
from task.models import Task, Group
from gql.gql_types import (
    UserCreateType,
    UserUpdateType,
    RoleCreateType,
    RoleUpdateType,
    OrganizationCreateType,
    OrganizationUpdateType,
    ProjectCreateType,
    ProjectUpdateType,
    TaskCreateType,
    TaskUpdateType,
    GroupUpdateType,
    GroupCreateType,
    RoleType,
    OrganizationType,
    ProjectType,
    TaskType,
    GroupType,
    UserType,
    GoogleRegDTO,
)
from utils import hash_user_pwd
from gql.graphql_utils import (
    process_task_assignees,
    strawberry_insert,
    decrease_task_time_by_id,
    strawberry_update,
    strawberry_delete,
    process_project_staff,
    task_preprocess,
)
from db.utils import get_user_by_id, full_delete_group, full_delete_user
from google_auth.andoroid_auth import google_register


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def change_password(
        self, new_password: str, change_password_token: str
    ) -> bool:
        async with get_redis() as redis:
            user_id = await get_user_id_from_reset_pwd_token(
                redis, change_password_token
            )
        user = await get_user_by_id(user_id)
        await set_new_pwd(user, new_password)
        return True

    @strawberry.mutation
    async def confirm_account(self, info: Info, user_id: UUID) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_insert(Role)
    async def add_role(self, info: Info, data: RoleCreateType) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_update(Role)
    async def update_role(
        self, info: Info, item_id: int, data: RoleUpdateType
    ) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_delete(Role)
    async def delete_role(self, info: Info, item_id: int) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_insert(
        User,
        process_extra_db=hash_user_pwd,
        exc_fields=["password"],
        notify_kwargs={"email_confirmation_token": secrets.token_urlsafe(32)},
        notify_from_data_kwargs={"email": "email"},
        notify_subject="email.confirmation",
        need_validation=False,
    )
    async def add_user(self, info: Info, data: UserCreateType) -> UserType:
        pass

    @strawberry.mutation
    @google_register
    async def google_register(self, info: Info, data: GoogleRegDTO) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_update(User)
    async def update_user(
        self, info: Info, item_id: UUID, data: UserUpdateType
    ) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_delete(User)
    async def delete_user(self, info: Info, item_id: UUID) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_delete(User, del_func=full_delete_user)
    async def full_delete_user(self, info: Info, item_id: UUID) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_insert(
        Organization, process_extra_db=process_project_staff, exc_fields=["staff"]
    )
    async def add_organization(
        self, info: Info, data: OrganizationCreateType
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_update(Organization)
    async def update_organization(
        self, info: Info, item_id: int, data: OrganizationUpdateType
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_delete(Organization)
    async def delete_organization(self, info: Info, item_id: int) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_insert(Project)
    async def add_project(self, info: Info, data: ProjectCreateType) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_update(Project)
    async def update_project(
        self, info: Info, item_id: int, data: ProjectUpdateType
    ) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_delete(Project)
    async def delete_project(self, info: Info, item_id: int) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_insert(
        Task,
        data_process_extra=task_preprocess,
        process_extra_db=process_task_assignees,
        exc_fields=["assignees"],
    )
    async def add_task(self, info: Info, data: TaskCreateType) -> TaskType:
        pass

    @strawberry.mutation
    @strawberry_update(Task)
    async def update_task(
        self, info: Info, item_id: int, data: TaskUpdateType
    ) -> TaskType:
        pass

    @strawberry.mutation
    @strawberry_delete(Task)
    async def delete_task(self, info: Info, item_id: int) -> TaskType:
        pass

    @strawberry.mutation
    async def decrease_task_time(self, item_id: int, seconds: int) -> bool:
        await decrease_task_time_by_id(item_id, seconds)
        return True

    @strawberry.mutation
    @strawberry_insert(Group)
    async def add_group(self, info: Info, data: GroupCreateType) -> GroupType:
        pass

    @strawberry.mutation
    @strawberry_update(Group)
    async def update_group(
        self, info: Info, item_id: int, data: GroupUpdateType
    ) -> GroupType:
        pass

    @strawberry.mutation
    @strawberry_delete(Group, del_func=full_delete_group)
    async def delete_group(
        self, info: Info, item_id: int
    ) -> GroupType:
        pass
