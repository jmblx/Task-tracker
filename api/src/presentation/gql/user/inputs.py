from uuid import UUID

import strawberry


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
class UserUpdateType:
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    email: str | None = None
    tg_id: str | None = None
    tg_settings: strawberry.scalars.JSON | None = None
    github_name: str | None = None
