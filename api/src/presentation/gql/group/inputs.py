from uuid import UUID

import strawberry


@strawberry.input
class GroupFindType:
    id: int | None = None
    name: str | None = None
    user_id: UUID | None = None
    project_id: int | None = None


@strawberry.input
class GroupCreateType:
    name: str
    user_id: UUID
    project_id: int | None = None


@strawberry.input
class GroupUpdateType:
    name: str | None = None
    user_id: UUID | None = None
    project_id: int | None = None
