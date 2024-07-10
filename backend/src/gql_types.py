from typing import Optional, List
from uuid import UUID

import strawberry
from sqlalchemy.orm import joinedload
from strawberry import Info

from auth.models import User
from auth.task_read_schema import TaskRead
from task.group_schemas import GroupFind, GroupUpdate, GroupCreate, GroupRead
from task.schemas import TaskUpdate, TaskFind, TaskSchema
from auth.schemas import UserRead, UserFind, UserUpdate, UserSchema, RoleRead, UserCreate, RoleSchema, RoleUpdate, \
    RoleFind
from organization.schemas import (
    OrganizationRead, OrganizationFind, OrganizationCreate, OrganizationUpdate
)
from project.schemas import ProjectFind, ProjectRead, ProjectCreate, ProjectUpdate
from scalars import DateTime, Duration
from utils import find_obj


@strawberry.input
class UserAssigneeType:
    id: UUID
    organization_id: int
    github_data: Optional[strawberry.scalars.JSON]


@strawberry.experimental.pydantic.type(model=RoleRead, fields=["id", "name"])
class RoleReadType:
    permissions: strawberry.scalars.JSON


@strawberry.experimental.pydantic.input(model=RoleFind, fields=["id", "name"])
class RoleFindType:
    pass


@strawberry.experimental.pydantic.input(model=RoleUpdate, fields=["name"])
class RoleUpdateType:
    permissions: Optional[strawberry.scalars.JSON]


@strawberry.experimental.pydantic.input(model=RoleSchema, fields=["name"])
class RoleCreateType:
    permissions: strawberry.scalars.JSON


@strawberry.experimental.pydantic.type(model=TaskSchema, fields=[
    'id', 'name', 'description', 'is_done', 'added_at', 'done_at',
    'color', 'difficulty', 'project_id', 'group_id'])
class TaskType:
    duration: Duration
    assignees: List["UserType"]


@strawberry.experimental.pydantic.type(model=ProjectRead, all_fields=True)
class ProjectType:
    pass


@strawberry.experimental.pydantic.input(model=UserFind, fields=[
    'id', 'first_name', 'last_name', 'email'
])
class UserFindType:
    pass


# @strawberry.experimental.pydantic.type(model=UserRead, fields=[
#     'first_name', 'last_name', 'role_id', 'email', 'is_active', 'is_superuser',
#     'is_verified', 'pathfile', 'role', 'tg_id', 'id', "tasks"
# ])
# class UserType:
#     # Используем strawberry.scalars.JSON для tg_settings
#     tg_settings: Optional[strawberry.scalars.JSON]

@strawberry.experimental.pydantic.type(model=UserRead, fields=[
    'first_name', 'last_name', 'role_id', 'email', 'is_active', 'is_superuser',
    'is_verified', 'pathfile', 'tg_id', 'id', "tasks"
])
class UserType:
    @strawberry.field
    async def role(self, info: Info) -> Optional[RoleReadType]:
        role_loader = info.context["role_loader"]
        user = await info.context["user_loader"].load(self.id)
        if user and user.role_id:
            role = await role_loader.load(user.role_id)
            return RoleReadType.from_pydantic(role)
        return None

    @strawberry.field
    async def tasks(self, info: Info) -> List["TaskType"]:
        task_loader = info.context["task_loader"]
        tasks = await task_loader.load(self.id)
        return [TaskType.from_pydantic(TaskRead.from_orm(task)) for task in tasks]

    @strawberry.field
    async def tasks_assigned(self, info: Info) -> List[TaskType]:
        task_loader = info.context["task_loader"]
        tasks = await task_loader.load(self.id, is_assigned=True)
        return [TaskType.from_pydantic(task) for task in tasks]


@strawberry.experimental.pydantic.type(model=UserCreate, fields=[
    'first_name', 'last_name', 'role_id', 'email', 'password', 'is_active',
    'is_superuser', 'is_verified', 'pathfile', 'tg_id', 'github_name'
])
class UserCreateType:
    tg_settings: strawberry.scalars.JSON

@strawberry.experimental.pydantic.input(model=UserUpdate, fields=[
    'first_name', 'last_name', 'role_id', 'email', 'tg_id'
])
class UserUpdateType:
    tg_settings: strawberry.scalars.JSON


@strawberry.experimental.pydantic.type(model=OrganizationRead, all_fields=True)
class OrganizationType:
    pass


@strawberry.experimental.pydantic.input(model=OrganizationFind, all_fields=True)
class OrganizationFindType:
    pass


@strawberry.experimental.pydantic.input(model=OrganizationCreate, all_fields=True)
class OrganizationCreateType:
    pass


@strawberry.experimental.pydantic.input(model=OrganizationUpdate, all_fields=True)
class OrganizationUpdateType:
    pass


@strawberry.experimental.pydantic.input(model=TaskFind, all_fields=True)
class TaskFindType:
    pass


@strawberry.input
class TaskCreateType:
    name: str
    description: Optional[str]
    is_done: Optional[bool]
    assigner_id: UUID
    color: Optional[str]
    duration: Duration
    difficulty: Optional[str]
    project_id: int
    group_id: Optional[int]
    assignees: Optional[List[UserAssigneeType]]

@strawberry.experimental.pydantic.type(model=TaskRead, fields=[
    'id', 'name', 'description', 'is_done', 'assigner_id', 'color', 'difficulty', 'project_id', 'assignees', 'assigner'])
class TaskReadType:
    added_at: DateTime
    done_at: DateTime
    duration: Duration

@strawberry.experimental.pydantic.input(model=TaskUpdate, fields=[
    'name', 'description', 'is_done', 'assigner_id', 'color', 'difficulty', 'project_id'])
class TaskUpdateType:
    added_at: Optional[DateTime] = None
    done_at: Optional[DateTime] = None
    duration: Optional[Duration]


@strawberry.input()
class TaskDecreaseTime:
    seconds: int


@strawberry.experimental.pydantic.type(model=UserSchema, fields=[
    'id',
    'first_name', 'last_name', 'role_id', 'email', 'is_active', 'is_superuser',
    'is_verified', 'pathfile', 'tg_id', 'organization_id',
    'is_email_confirmed', 'registered_at'
])
class UserReadType:
    tg_settings: strawberry.scalars.JSON
    role: Optional[RoleReadType]
    tasks: Optional[List[TaskType]]


@strawberry.experimental.pydantic.input(model=ProjectFind, all_fields=True)
class ProjectFindType:
    pass


@strawberry.experimental.pydantic.input(model=ProjectCreate, all_fields=True)
class ProjectCreateType:
    pass


@strawberry.experimental.pydantic.input(model=ProjectUpdate, all_fields=True)
class ProjectUpdateType:
    pass


@strawberry.experimental.pydantic.type(model=GroupRead, all_fields=True)
class GroupType:
    pass


@strawberry.experimental.pydantic.input(model=GroupFind, all_fields=True)
class GroupFindType:
    pass


@strawberry.experimental.pydantic.input(model=GroupCreate, all_fields=True)
class GroupCreateType:
    pass


@strawberry.experimental.pydantic.input(model=GroupUpdate, all_fields=True)
class GroupUpdateType:
    pass


# class TaskReadSchema:
#     id: int = Field(int)
#     description: str = Field(str)
#     is_done: bool = Field(bool)
#     added_at: datetime = Field(datetime)
#     done_at: Optional[datetime] = Field(datetime, default=None)
#     color: str = Field(str)
#     difficulty: str = Field(str)
#     assignees: Optional[List[UserSchemaType]] = Field(List[UserSchemaType], default=None)
#     assigner: Optional[UserSchemaType] = Field(UserSchemaType, default=None)

