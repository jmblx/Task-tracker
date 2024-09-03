import strawberry
from strawberry import Info

from domain.entities.organization.models import Organization
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.organization.inputs import OrganizationFindType
from presentation.gql.organization.types import OrganizationType


@strawberry.type
class OrganizationQuery:
    @strawberry.field
    @strawberry_read(
        Organization, OrganizationType, "getOrganization", need_validation=True
    )
    async def get_organization(
        self,
        info: Info,
        search_data: OrganizationFindType,
        order_by: OrderByInput | None = None,
    ) -> list[OrganizationType] | None:
        pass
