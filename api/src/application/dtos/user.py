from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from application.dtos.base import BaseDTO


@dataclass
class UserCreateDTO(BaseDTO):
    first_name: str
    last_name: str
    email: str
    password: str = field(repr=False)
    hashed_password: str = field(init=False, default="")
    role_id: int | None = None
    is_active: bool = True
    is_verified: bool = False
    pathfile: str | None = None
    tg_id: str | None = None
    tg_settings: dict | None = None
    github_name: str | None = None


@dataclass
class UserReadDTO(BaseDTO):
    id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    email: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    pathfile: str | None = None
    tg_id: str | None = None
    tg_settings: dict | None = None
    is_email_confirmed: bool | None = None
    registered_at: datetime | None = None
    organizations: list[dict] | None = None
    role: dict | None = None
    tasks: list[dict] | None = None
