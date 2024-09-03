import strawberry


@strawberry.input
class UserAuthType:
    email: str
    password: str


@strawberry.input
class GoogleRegDTO:
    email: str
    given_name: str
    family_name: str | None = None
    email_verified: bool
