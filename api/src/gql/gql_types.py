from typing import Optional
from uuid import UUID

import strawberry
from strawberry.scalars import JSON

from gql.graphql_utils import add_from_instance
from gql.scalars import DateTime, Duration
from utils import GqlProtocol


@strawberry.type
@add_from_instance
class RoleType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    permissions: strawberry.scalars.JSON | None = None


@strawberry.input
class RoleFindType:
    id: int | None = None
    name: str | None = None


@strawberry.input
class RoleCreateType:
    name: str
    permissions: strawberry.scalars.JSON


@strawberry.input
class RoleUpdateType:
    name: str | None = None
    permissions: strawberry.scalars.JSON | None = None


@strawberry.input
class UserAuthType:
    email: str
    password: str


# Типы для User
@strawberry.type
@add_from_instance
class UserType(GqlProtocol):
    id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    email: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    pathfile: str | None = None
    tg_id: str | None = None
    tg_settings: strawberry.scalars.JSON | None = None
    is_email_confirmed: bool | None = None
    registered_at: DateTime | None = None
    organizations: list["OrganizationType"] | None = None
    role: RoleType | None = None
    tasks: list["TaskType"] | None = None  # Using string annotation here


@strawberry.input
class UserFindType:
    id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


@strawberry.input
class UserCreateType:
    first_name: str
    last_name: str
    role_id: int
    email: str
    password: str
    is_active: bool | None = True
    is_verified: bool | None = True
    pathfile: str | None = None
    tg_id: str | None = None
    tg_settings: strawberry.scalars.JSON | None = None
    github_name: str | None = None


@strawberry.input
class GoogleRegDTO:
    email: str
    given_name: str
    family_name: str | None = None
    email_verified: bool


@strawberry.input
class UserUpdateType:
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    email: str | None = None
    tg_id: str | None = None
    tg_settings: strawberry.scalars.JSON | None = None
    github_name: str | None = None


@strawberry.type
@add_from_instance
class TaskType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    is_done: bool | None = None
    added_at: DateTime | None = None
    done_at: DateTime | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    duration: Duration | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None
    assignees: list["UserType"] | None = None
    assigner: Optional["UserType"] = None


@strawberry.input
class TaskFindType:
    id: int | None = None
    name: str | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None


@strawberry.input
class AssigneeType:
    id: UUID | None = None
    github_data: JSON | None = None
    organization_id: int | None = None


@strawberry.input
class TaskCreateType:
    name: str
    description: str | None = None
    is_done: bool | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    duration: Duration
    end_date: DateTime | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None
    assignees: list[AssigneeType] | None = None


@strawberry.input
class TaskUpdateType:
    name: str | None = None
    description: str | None = None
    is_done: bool | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    duration: Duration | None = None
    end_date: DateTime | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None


@strawberry.type
@add_from_instance
class OrganizationType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    staff: list[UserType] | None = None
    # workers: Optional[List[UserType]] = None
    # managers: Optional[List[UserType]] = None
    projects: list["ProjectType"] | None = None


@strawberry.input
class OrganizationFindType:
    id: int | None = None
    name: str | None = None
    owner_id: UUID | None = None


@strawberry.input
class StaffType:
    id: UUID
    position: str
    permissions: JSON


@strawberry.input
class OrganizationCreateType:
    name: str
    description: str
    staff: list[StaffType] | None = None


@strawberry.input
class OrganizationUpdateType:
    name: str | None = None
    description: str | None = None
    staff: list[UUID] | None = None


@strawberry.type
@add_from_instance
class ProjectType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    created_at: DateTime | None = None
    organization_id: int | None = None
    tasks: list[TaskType] | None = None  # Using actual TaskType here


@strawberry.input
class ProjectFindType:
    id: int | None = None
    name: str | None = None


@strawberry.input
class ProjectCreateType:
    name: str
    description: str | None = None
    organization_id: int


@strawberry.input
class ProjectUpdateType:
    name: str | None = None
    description: str | None = None
    organization_id: int | None = None


@strawberry.type
@add_from_instance
class GroupType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    tasks: list[TaskType] | None = None
    user: UserType | None = None


@strawberry.input
class GroupFindType:
    id: int | None = None
    name: str | None = None
    user_id: UUID | None = None


@strawberry.input
class GroupCreateType:
    name: str
    user_id: UUID


@strawberry.input
class GroupUpdateType:
    name: str | None = None
    user_id: UUID | None = None


@strawberry.input
class OrderByInput:
    field: str
    direction: str
