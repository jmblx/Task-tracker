import strawberry


@strawberry.input
class OrderByInput:
    field: str
    direction: str
