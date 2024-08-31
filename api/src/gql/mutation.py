import secrets
from uuid import UUID

import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from entities.user.models import Role, User
from db.utils import full_delete_group, full_delete_user
from gql.gql_types import (
    GroupCreateType,
    GroupType,
    GroupUpdateType,
    OrganizationCreateType,
    OrganizationType,
    OrganizationUpdateType,
    ProjectCreateType,
    ProjectType,
    ProjectUpdateType,
    RoleCreateType,
    RoleType,
    RoleUpdateType,
    TaskCreateType,
    TaskType,
    TaskUpdateType,
    UserCreateType,
    UserType,
    UserUpdateType,
)
from gql.graphql_utils import (
    decrease_task_time_by_id,
    process_project_staff,
    process_task_assignees,
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
    task_preprocess,
)
from myredis.utils import get_user_id_from_reset_pwd_token
from entities.organization.models import Organization
from entities.project.models import Project
from entities.task.models import Group, Task
from utils import hash_user_pwd


@strawberry.type
class Mutation:
    @strawberry.mutation
    @strawberry_insert(Role)
    async def add_role(self, info: Info, data: RoleCreateType) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_update(Role)
    async def update_role(
        self, info: Info, item_id: int, data: RoleUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Role)
    async def update_role_with_response(
        self, info: Info, item_id: int, data: RoleUpdateType
    ) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_delete(Role)
    async def delete_role(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Role)
    async def delete_role_with_response(
        self, info: Info, item_id: int
    ) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_insert(
        User,
        process_extra_db=hash_user_pwd,
        exc_fields=["password"],
        notify_kwargs={"email_confirmation_token": secrets.token_urlsafe(32)},
        notify_from_data_kwargs={"email": "email"},
        notify_subject="email.confirmation",
        validation=False,
    )
    async def add_user(self, info: Info, data: UserCreateType) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_update(User)
    async def update_user(
        self, info: Info, item_id: UUID, data: UserUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(User)
    async def update_user_with_response(
        self, info: Info, item_id: int, data: UserUpdateType
    ) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_delete(User)
    async def delete_user(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(User)
    async def delete_user_with_response(
        self, info: Info, item_id: UUID
    ) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_delete(User, del_func=full_delete_user)
    async def full_delete_user(self, info: Info, item_id: UUID) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_insert(
        Organization,
        process_extra_db=process_project_staff,
        exc_fields=["staff"],
    )
    async def add_organization(
        self, info: Info, data: OrganizationCreateType
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_update(Organization)
    async def update_organization(
        self, info: Info, item_id: int, data: OrganizationUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Organization)
    async def update_organization_with_response(
        self, info: Info, item_id: int, data: OrganizationUpdateType
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_delete(Organization)
    async def delete_organization(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Organization)
    async def delete_organization_with_response(
        self, info: Info, item_id: int
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_insert(Project)
    async def add_project(
        self, info: Info, data: ProjectCreateType
    ) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_update(Project)
    async def update_project(
        self, info: Info, item_id: int, data: ProjectUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Project)
    async def update_project_with_response(
        self, info: Info, item_id: int, data: ProjectUpdateType
    ) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_delete(Project)
    async def delete_project(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Project)
    async def delete_project_with_response(
        self, info: Info, item_id: int
    ) -> ProjectType:
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
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Task)
    async def update_task_with_response(
        self, info: Info, item_id: int, data: TaskUpdateType
    ) -> TaskType:
        pass

    @strawberry.mutation
    @strawberry_delete(Task)
    async def delete_task(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Task)
    async def delete_task_with_response(
        self, info: Info, item_id: int
    ) -> TaskType:
        pass

    @strawberry.mutation
    async def decrease_task_time(
        self, info: Info, item_id: int, seconds: int
    ) -> bool:
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
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Group)
    async def update_group_with_response(
        self, info: Info, item_id: int, data: GroupUpdateType
    ) -> GroupType:
        pass

    @strawberry.mutation
    @strawberry_delete(Group)
    async def delete_group(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Group, del_func=full_delete_group)
    async def delete_group_with_response(
        self, info: Info, item_id: int
    ) -> GroupType:
        pass
