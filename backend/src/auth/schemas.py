import uuid
import datetime
from typing import Optional, List

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Any, Dict

from task.schemas import TaskSchema


class UserSchema(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    first_name: str
    last_name: str
    role_id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    pathfile: Optional[str] = None
    role: "RoleRead"
    tg_id: Optional[str] = None
    tg_settings: Optional[Dict[str, Any]] = None
    organization_id: Optional[int]
    is_email_confirmed: bool
    registered_at: datetime.datetime
    tasks: Optional[List["TaskSchema"]] = None

    class Config:
        from_attributes = True


class UserFind(BaseModel):
    id: Optional[uuid.UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    role_id: int
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    pathfile: Optional[str] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[dict] = None
    github_name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None
    email: Optional[EmailStr] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[dict] = None
    github_name: Optional[str] = None


class UserGoogleRegistration(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None


class RoleSchema(BaseModel):
    name: str
    permissions: Dict[str, Any]

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None


class RoleFind(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class RoleRead(RoleSchema):
    id: int

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    registered_at: datetime.datetime
    role_id: int
    pathfile: Optional[str] = None
    tg_id: Optional[str] = None
    tg_settings: Optional[dict] = None
    organization_id: Optional[int] = None
    is_email_confirmed: bool
    role: Optional[RoleRead] = None
    tasks: Optional[List["TaskSchema"]] = None

    class Config:
        from_attributes = True
