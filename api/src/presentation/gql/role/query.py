import strawberry
from strawberry import Info

from application.usecases.role.read import ReadRoleUseCase
from core.db.utils import get_selected_fields
from core.di.container import container
from domain.entities.role.models import Role
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.role.inputs import RoleFindType
from presentation.gql.role.types import RoleType


@strawberry.type
class RoleQuery:
    @strawberry.field
    async def get_role(
        self,
        info: Info,
        search_data: RoleFindType,
        order_by: OrderByInput | None = None,
    ) -> list[RoleType] | None:
        async with container() as ioc:
            interactor = await ioc.get(ReadRoleUseCase)
            selected_fields = get_selected_fields(info, "getRole")
            roles = await interactor(
                search_data.__dict__, selected_fields, order_by
            )
            return [RoleType.from_instance(role, selected_fields) for role in roles]