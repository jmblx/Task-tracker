import uuid
import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Any, Dict


class UserSchema(schemas.BaseUser[uuid.UUID]):

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

    class Config:
        from_attributes = True


class UserFind(BaseModel):
    id: Optional[uuid.UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(schemas.BaseUserCreate):
    # схема pydantic для взаимодействия с регистрацией
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


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: Optional[int]
    email: Optional[EmailStr]
    tg_id: Optional[str] = None
    tg_settings: Optional[dict] = None


class UserGoogleRegistration(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None


class RoleSchema(BaseModel):
    name: str
    permissions: Dict[str, Any]


class RoleRead(RoleSchema):
    id: int


class UserRead(schemas.BaseUser[uuid.UUID]):

    first_name: str
    last_name: str
    role_id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    pathfile: Optional[str] = None
    role: RoleRead
    tg_id: Optional[str] = None
    tg_settings: Optional[dict] = None

    class Config:
        from_attributes = True



