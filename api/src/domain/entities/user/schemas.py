import uuid
from typing import Any

from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserFind(BaseModel):
    id: uuid.UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserGoogleRegistration(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    phone_number: str | None = None


class RoleSchema(BaseModel):
    name: str
    permissions: dict[str, Any]

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    name: str | None = None
    permissions: dict[str, Any] | None = None


class RoleFind(BaseModel):
    id: int | None = None
    name: str | None = None

    class Config:
        from_attributes = True


class RoleRead(RoleSchema):
    id: int

    class Config:
        from_attributes = True
