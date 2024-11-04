import strawberry
from strawberry import Info

from application.usecases.organization.read import ReadOrganizationUseCase
from core.di.container import container
from domain.entities.organization.models import Organization
from core.db.utils import get_selected_fields
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.organization.inputs import OrganizationFindType
from presentation.gql.organization.types import OrganizationType


@strawberry.type
class OrganizationQuery:
    @strawberry.field
    async def get_organization(
        self,
        info: Info,
        search_data: OrganizationFindType,
        order_by: OrderByInput | None = None,
    ) -> list[OrganizationType] | None:
        async with container() as ioc:
            interactor = await ioc.get(ReadOrganizationUseCase)
            selected_fields = get_selected_fields(info, "getOrganization")
            organizations = await interactor(
                search_data.__dict__, selected_fields, order_by
            )
            return [OrganizationType.from_instance(org, selected_fields) for org in organizations]
