import strawberry
from strawberry import Info

from domain.entities.role.models import Role
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.role.inputs import RoleFindType
from presentation.gql.role.types import RoleType


@strawberry.type
class RoleQuery:
    @strawberry.field
    @strawberry_read(Role, RoleType, "getRole", need_validation=True)
    async def get_role(
        self,
        info: Info,
        search_data: RoleFindType,
        order_by: OrderByInput | None = None,
    ) -> list[RoleType] | None:
        pass
