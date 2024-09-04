from dataclasses import dataclass, field

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
