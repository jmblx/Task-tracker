from uuid import UUID

import strawberry
from strawberry.scalars import JSON


@strawberry.input
class OrganizationFindType:
    id: int | None = None
    name: str | None = None
    owner_id: UUID | None = None


@strawberry.input
class StaffType:
    id: UUID
    position: str
    permissions: JSON


@strawberry.input
class OrganizationCreateType:
    name: str
    description: str
    staff: list[StaffType] | None = None


@strawberry.input
class OrganizationUpdateType:
    name: str | None = None
    description: str | None = None
    staff: list[UUID] | None = None
