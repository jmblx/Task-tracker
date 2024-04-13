from typing import Optional, List
import datetime

import strawberry
from strawberry.schema.types.concrete_type import Field

from auth.schemas import UserRead, UserFind, UserUpdate, UserSchema, RoleRead, UserCreate
from organization.schemas import (
    OrganizationRead, OrganizationFind, OrganizationCreate, OrganizationUpdate
)
from project.schemas import ProjectFind, ProjectRead, ProjectCreate, ProjectUpdate
from task.schemas import TaskCreate, TaskUpdate, TaskFind, TaskRead


@strawberry.experimental.pydantic.type(model=RoleRead, fields=["name", "id"])
class RoleReadType:
    permissions: strawberry.scalars.JSON


@strawberry.experimental.pydantic.type(model=UserSchema, fields=[
    'first_name', 'last_name', 'role_id', 'email', 'is_active', 'is_superuser',
    'is_verified', 'pathfile', 'role', 'tg_id', 'organization_id',
    'is_email_confirmed', 'registered_at'
])
class UserType:
    tg_settings: strawberry.scalars.JSON


# @strawberry.type
# class UserSchemaType:
#     first_name: str
#     last_name: str
#     role_id: int
#     email: str
#     is_active: bool = True
#     is_superuser: bool = False
#     is_verified: bool = False
#     pathfile: Optional[str] = None
#     role: "RoleRead"
#     tg_id: Optional[str] = None
#     tg_settings: Optional[dict] = None
#     organization_id: Optional[int]
#     is_email_confirmed: bool
#     registered_at: datetime.datetime


@strawberry.experimental.pydantic.input(model=UserFind, fields=[
    'id', 'first_name', 'last_name', 'email'
])
class UserFindType:
    pass


@strawberry.experimental.pydantic.type(model=UserRead, fields=[
    'first_name', 'last_name', 'role_id', 'email', 'is_active', 'is_superuser',
    'is_verified', 'pathfile', 'role', 'tg_id'
])
class UserReadType:
    # Используем strawberry.scalars.JSON для tg_settings
    tg_settings: Optional[strawberry.scalars.JSON]


@strawberry.experimental.pydantic.type(model=UserCreate, fields=[
    'first_name', 'last_name', 'role_id', 'email', 'password', 'is_active',
    'is_superuser', 'is_verified', 'pathfile', 'tg_id'
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


@strawberry.experimental.pydantic.type(model=ProjectRead, all_fields=True)
class ProjectType:
    pass


@strawberry.experimental.pydantic.input(model=ProjectFind, all_fields=True)
class ProjectFindType:
    pass


@strawberry.experimental.pydantic.input(model=ProjectCreate, all_fields=True)
class ProjectCreateType:
    pass


@strawberry.experimental.pydantic.input(model=ProjectUpdate, all_fields=True)
class ProjectUpdateType:
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

@strawberry.experimental.pydantic.type(model=TaskRead, all_fields=True)
class TaskType:
    pass


@strawberry.experimental.pydantic.input(model=TaskFind, all_fields=True)
class TaskFindType:
    pass


@strawberry.experimental.pydantic.input(model=TaskCreate, all_fields=True)
class TaskCreateType:
    pass


@strawberry.experimental.pydantic.input(model=TaskUpdate, all_fields=True)
class TaskUpdateType:
    pass

# @strawberry.experimental.pydantic.type(model=EventResponse)
# class EventType:
#     id: strawberry.auto
#     title: strawberry.auto
#     description: strawberry.auto
#     img_path: strawberry.auto
#     address: strawberry.auto
#     category: CategoryType
#
#
# @strawberry.experimental.pydantic.input(model=EventAdd, all_fields=True)
# class EventInputType:
#     pass
#
#
# @strawberry.experimental.pydantic.input(model=EventUpdate, all_fields=True)
# class EventUpdateType:
#     pass
#
#
# @strawberry.experimental.pydantic.input(model=EventGet, all_fields=True)
# class EventGetType:
#     pass
