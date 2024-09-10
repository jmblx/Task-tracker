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


@strawberry.input
class FullNameType:
    first_name: str
    last_name: str

    def to_dict(self):
        return (
            {"first_name": self.first_name, "last_name": self.last_name}
            if self.last_name and self.first_name
            else None
        )
