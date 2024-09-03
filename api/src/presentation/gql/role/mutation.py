import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from domain.entities.role.models import Role
from presentation.gql.graphql_utils import (
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
)
from presentation.gql.role.inputs import RoleCreateType, RoleUpdateType
from presentation.gql.role.types import RoleType


@strawberry.type
class RoleMutation:
    @strawberry.mutation
    @strawberry_insert(Role)
    async def add_role(self, info: Info, data: RoleCreateType) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_update(Role)
    async def update_role(
        self, info: Info, item_id: int, data: RoleUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Role)
    async def update_role_with_response(
        self, info: Info, item_id: int, data: RoleUpdateType
    ) -> RoleType:
        pass

    @strawberry.mutation
    @strawberry_delete(Role)
    async def delete_role(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Role)
    async def delete_role_with_response(
        self, info: Info, item_id: int
    ) -> RoleType:
        pass
