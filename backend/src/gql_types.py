from typing import Optional, List, get_type_hints
from uuid import UUID

import strawberry
from strawberry import scalars

from scalars import DateTime, Duration
from utils import add_from_instance


# Типы для Role
@strawberry.type
@add_from_instance
class RoleType:
    id: Optional[int]
    name: Optional[str]
    permissions: Optional[strawberry.scalars.JSON]


@strawberry.input
class RoleFindType:
    id: Optional[int] = None
    name: Optional[str] = None


@strawberry.input
class RoleCreateType:
    name: str
    permissions: strawberry.scalars.JSON


@strawberry.input
class RoleUpdateType:
    name: Optional[str] = None
    permissions: Optional[strawberry.scalars.JSON] = None


# Типы для User
@strawberry.type
@add_from_instance
class UserType:
    id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    pathfile: Optional[str] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[strawberry.scalars.JSON] = None
    organization_id: Optional[int] = None
    is_email_confirmed: Optional[bool] = None
    registered_at: Optional[DateTime] = None
    organization: Optional["OrganizationType"] = None
    role: Optional[RoleType] = None
    tasks: Optional[List["TaskType"]] = None  # Using string annotation here


@strawberry.input
class UserFindType:
    id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


@strawberry.input
class UserCreateType:
    first_name: str
    last_name: str
    role_id: int
    email: str
    password: str
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    pathfile: Optional[str] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[strawberry.scalars.JSON] = None
    github_name: Optional[str] = None


@strawberry.input
class UserUpdateType:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None
    email: Optional[str] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[strawberry.scalars.JSON] = None
    github_name: Optional[str] = None


@strawberry.type
@add_from_instance
class TaskType:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    added_at: Optional[DateTime] = None
    done_at: Optional[DateTime] = None
    assigner_id: Optional[UUID] = None
    color: Optional[str] = None
    duration: Optional[Duration] = None
    difficulty: Optional[str] = None
    project_id: Optional[int] = None
    group_id: Optional[int] = None
    assignees: Optional[List["UserType"]] = None
    assigner: Optional["UserType"] = None

    @classmethod
    def from_instance_no_assignees(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            is_done=instance.is_done,
            added_at=instance.added_at,
            done_at=instance.done_at,
            assigner_id=instance.assigner_id,
            color=instance.color,
            duration=instance.duration,
            difficulty=instance.difficulty,
            project_id=instance.project_id,
            group_id=instance.group_id,
            assignees=None,  # No assignees loaded
        )


@strawberry.input
class TaskFindType:
    id: Optional[int] = None
    name: Optional[str] = None
    assigner_id: Optional[UUID] = None
    color: Optional[str] = None
    difficulty: Optional[str] = None
    project_id: Optional[int] = None
    group_id: Optional[int] = None


@strawberry.input
class TaskCreateType:
    name: str
    description: Optional[str] = None
    is_done: Optional[bool] = None
    assigner_id: UUID
    color: Optional[str] = None
    duration: Duration
    difficulty: Optional[str] = None
    project_id: int
    group_id: Optional[int] = None
    assignees: Optional[List[strawberry.scalars.JSON]] = None


@strawberry.input
class TaskUpdateType:
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    assigner_id: Optional[UUID] = None
    color: Optional[str] = None
    duration: Optional[Duration] = None
    difficulty: Optional[str] = None
    project_id: Optional[int] = None
    group_id: Optional[int] = None


@strawberry.type
@add_from_instance
class OrganizationType:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    staff: Optional[List[UserType]] = None
    # workers: Optional[List[UserType]] = None
    # managers: Optional[List[UserType]] = None
    projects: Optional[List["ProjectType"]] = None


@strawberry.input
class OrganizationFindType:
    id: Optional[int] = None
    name: Optional[str] = None


@strawberry.input
class OrganizationCreateType:
    name: str
    description: str


@strawberry.input
class OrganizationUpdateType:
    name: Optional[str] = None
    description: Optional[str] = None


@strawberry.type
@add_from_instance
class ProjectType:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[DateTime] = None
    organization_id: Optional[int] = None
    tasks: Optional[List[TaskType]] = None  # Using actual TaskType here


@strawberry.input
class ProjectFindType:
    id: Optional[int] = None
    name: Optional[str] = None


@strawberry.input
class ProjectCreateType:
    name: str
    description: Optional[str] = None
    organization_id: int


@strawberry.input
class ProjectUpdateType:
    name: Optional[str] = None
    description: Optional[str] = None
    organization_id: Optional[int] = None


@strawberry.type
@add_from_instance
class GroupType:
    id: Optional[int] = None
    name: Optional[str] = None
    tasks: Optional[List[TaskType]] = None
    user: Optional[UserType] = None


@strawberry.input
class GroupFindType:
    id: Optional[int] = None
    name: Optional[str] = None
    user_id: Optional[UUID] = None


@strawberry.input
class GroupCreateType:
    name: str
    user_id: UUID


@strawberry.input
class GroupUpdateType:
    name: Optional[str] = None
    user_id: Optional[UUID] = None
