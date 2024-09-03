import strawberry
from strawberry import Info

from domain.entities.user.models import User
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.user.inputs import UserFindType
from presentation.gql.user.types import UserType


@strawberry.type
class UserQuery:
    @strawberry.field
    @strawberry_read(User, UserType, "getUser", need_validation=True)
    async def get_user(
        self,
        info: Info,
        search_data: UserFindType,
        order_by: OrderByInput | None = None,
    ) -> list[UserType] | None:
        pass
