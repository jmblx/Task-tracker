import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from domain.entities.organization.models import Organization
from presentation.gql.graphql_utils import (
    process_project_staff,
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
)
from presentation.gql.organization.inputs import (
    OrganizationCreateType,
    OrganizationUpdateType,
)
from presentation.gql.organization.query import OrganizationType


@strawberry.type
class OrganizationMutation:
    @strawberry.mutation
    @strawberry_insert(
        Organization,
        process_extra_db=process_project_staff,
        exc_fields=["staff"],
    )
    async def add_organization(
        self, info: Info, data: OrganizationCreateType
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_update(Organization)
    async def update_organization(
        self, info: Info, item_id: int, data: OrganizationUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Organization)
    async def update_organization_with_response(
        self, info: Info, item_id: int, data: OrganizationUpdateType
    ) -> OrganizationType:
        pass

    @strawberry.mutation
    @strawberry_delete(Organization)
    async def delete_organization(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Organization)
    async def delete_organization_with_response(
        self, info: Info, item_id: int
    ) -> OrganizationType:
        pass
