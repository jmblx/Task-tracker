import strawberry


@strawberry.input
class RoleFindType:
    id: int | None = None
    name: str | None = None


@strawberry.input
class RoleCreateType:
    name: str
    permissions: strawberry.scalars.JSON


@strawberry.input
class RoleUpdateType:
    name: str | None = None
    permissions: strawberry.scalars.JSON | None = None
