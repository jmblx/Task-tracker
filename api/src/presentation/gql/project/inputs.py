import strawberry


@strawberry.input
class ProjectFindType:
    id: int | None = None
    name: str | None = None


@strawberry.input
class ProjectCreateType:
    name: str
    description: str | None = None
    organization_id: int


@strawberry.input
class ProjectUpdateType:
    name: str | None = None
    description: str | None = None
    organization_id: int | None = None
