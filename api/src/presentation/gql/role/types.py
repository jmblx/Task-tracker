import strawberry

from core.utils import GqlProtocol
from presentation.gql.graphql_utils import add_from_instance


@strawberry.type
@add_from_instance
class RoleType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    permissions: strawberry.scalars.JSON | None = None
