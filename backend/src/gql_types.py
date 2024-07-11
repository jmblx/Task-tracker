from typing import Optional, List
from uuid import UUID

import strawberry
from scalars import DateTime, Duration

# Типы для Role
@strawberry.type
class RoleType:
    id: int
    name: str
    permissions: strawberry.scalars.JSON

    @classmethod
    def from_instance(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            permissions=instance.permissions,
        )

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
class UserType:
    id: UUID
    first_name: str
    role_id: int
    last_name: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    pathfile: Optional[str] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[strawberry.scalars.JSON] = None
    organization_id: Optional[int] = None
    is_email_confirmed: bool
    registered_at: DateTime
    role: Optional[RoleType] = None
    tasks: Optional[List["TaskType"]] = None  # Using string annotation here

    @classmethod
    def from_instance(cls, instance, selected_fields=None):
        selected_fields = selected_fields or {}
        return cls(
            id=instance.id,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            is_active=instance.is_active,
            is_superuser=instance.is_superuser,
            is_verified=instance.is_verified,
            pathfile=instance.pathfile,
            tg_id=instance.tg_id,
            tg_settings=instance.tg_settings,
            organization_id=instance.organization_id,
            is_email_confirmed=instance.is_email_confirmed,
            registered_at=instance.registered_at,
            role_id=instance.role_id,
            role=RoleType.from_instance(instance.role) if 'role' in selected_fields else None,
            tasks=[TaskType.from_instance_no_assignees(task) for task in instance.tasks] if 'tasks' in selected_fields else None,
        )

    @classmethod
    def from_instance_no_tasks(cls, instance, selected_fields=None):
        selected_fields = selected_fields or {}
        return cls(
            id=instance.id,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            is_active=instance.is_active,
            is_superuser=instance.is_superuser,
            is_verified=instance.is_verified,
            pathfile=instance.pathfile,
            tg_id=instance.tg_id,
            tg_settings=instance.tg_settings,
            organization_id=instance.organization_id,
            is_email_confirmed=instance.is_email_confirmed,
            registered_at=instance.registered_at,
            role_id=instance.role_id,
            role=RoleType.from_instance(instance.role) if 'role' in selected_fields else None,
            tasks=None,  # No tasks loaded
        )

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

# Типы для Task
@strawberry.type
class TaskType:
    id: int
    name: str
    description: Optional[str] = None
    is_done: Optional[bool] = None
    added_at: Optional[DateTime] = None
    done_at: Optional[DateTime] = None
    assigner_id: UUID
    color: Optional[str] = None
    duration: Duration
    difficulty: Optional[str] = None
    project_id: int
    group_id: Optional[int] = None
    assignees: Optional[List[UserType]] = None
    assigner: Optional[UserType] = None  # Using actual UserType here

    @classmethod
    def from_instance(cls, instance, selected_fields=None):
        selected_fields = selected_fields or {}
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            is_done=instance.is_done,
            added_at=instance.added_at,
            done_at=instance.done_at,
            assigner_id=instance.assigner_id,
            assigner=UserType.from_instance_no_tasks(instance.assigner) if 'assigner' in selected_fields else None,
            color=instance.color,
            duration=instance.duration,
            difficulty=instance.difficulty,
            project_id=instance.project_id,
            group_id=instance.group_id,
            assignees=[UserType.from_instance_no_tasks(user) for user in instance.assignees] if 'assignees' in selected_fields else None,
        )

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
    assignees: Optional[List[UUID]] = None

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

# Типы для Organization
@strawberry.type
class OrganizationType:
    id: int
    name: str
    description: str
    workers: Optional[List[UserType]] = None  # Using actual UserType here
    managers: Optional[List[UserType]] = None  # Using actual UserType here
    projects: Optional[List["ProjectType"]] = None  # Using string annotation here

    @classmethod
    def from_instance(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            workers=[UserType.from_instance_no_tasks(user) for user in instance.staff if user.role.name == "worker"],
            managers=[UserType.from_instance_no_tasks(user) for user in instance.staff if user.role.name == "manager"],
            projects=[ProjectType.from_instance(project) for project in instance.projects] if instance.projects else None,
        )

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

# Типы для Project
@strawberry.type
class ProjectType:
    id: int
    name: str
    description: str
    created_at: DateTime
    organization_id: int
    tasks: Optional[List[TaskType]] = None  # Using actual TaskType here

    @classmethod
    def from_instance(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            created_at=instance.created_at,
            organization_id=instance.organization_id,
            tasks=[TaskType.from_instance_no_assignees(task) for task in instance.tasks] if instance.tasks else None,
        )

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

# Типы для Group
@strawberry.type
class GroupType:
    id: int
    name: str
    tasks: Optional[List[TaskType]] = None
    user: Optional[UserType] = None

    @classmethod
    def from_instance(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            tasks=[TaskType.from_instance_no_assignees(task) for task in instance.tasks] if instance.tasks else None,
            user=UserType.from_instance_no_tasks(instance.user),
        )

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
