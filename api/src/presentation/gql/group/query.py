import strawberry
from strawberry import Info

from application.usecases.group.read import ReadGroupUseCase
from core.di.container import container
from core.utils import get_selected_fields
from presentation.gql.gql_types import OrderByInput
from presentation.gql.group.inputs import GroupFindType
from presentation.gql.group.types import GroupType


@strawberry.type
class GroupQuery:
    @strawberry.field
    async def get_group(
        self,
        info: Info,
        search_data: GroupFindType,
        order_by: OrderByInput | None = None,
    ) -> list[GroupType] | None:
        async with container() as ioc:
            interactor = await ioc.get(ReadGroupUseCase)
            selected_fields = get_selected_fields(info, "getGroup")
            groups = await interactor(
                search_data.__dict__, selected_fields, order_by
            )
            return [
                GroupType.from_instance(group, selected_fields)
                for group in groups
            ]
