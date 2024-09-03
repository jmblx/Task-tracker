import strawberry
from strawberry import Info

from domain.entities.group.models import Group
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.group.inputs import GroupFindType
from presentation.gql.group.types import GroupType


@strawberry.type
class GroupQuery:
    @strawberry.field
    @strawberry_read(Group, GroupType, "getGroup", need_validation=True)
    async def get_group(
        self,
        info: Info,
        search_data: GroupFindType,
        order_by: OrderByInput | None = None,
    ) -> list[GroupType] | None:
        pass
