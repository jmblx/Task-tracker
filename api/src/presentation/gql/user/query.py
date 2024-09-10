import strawberry
from strawberry import Info

from application.usecases.user.read import ReadUserUseCase
from core.db.utils import get_selected_fields
from core.di.container import container
from core.utils import (
    extract_selected_fields,
    convert_dict_top_level_to_snake_case,
    get_selected_fields,
)
from presentation.gql.gql_types import OrderByInput
from presentation.gql.user.inputs import UserFindType
from presentation.gql.user.types import UserType


# from strawberry import Info
#
# from domain.entities.user.models import User
# from presentation.gql.gql_types import OrderByInput
# from presentation.gql.graphql_utils import strawberry_read
# from presentation.gql.user.inputs import UserFindType
# from presentation.gql.user.types import UserType


@strawberry.type
class UserQuery:
    @strawberry.field
    async def get_user(
        self,
        info: Info,
        search_data: UserFindType,
        order_by: OrderByInput | None = None,
    ) -> list[UserType] | None:
        async with container() as ioc:
            interactor = await ioc.get(ReadUserUseCase)
            selected_fields = get_selected_fields(info, "getUser")
            users = await interactor(
                search_data.__dict__, selected_fields, order_by
            )
            return [
                UserType.from_instance(user, selected_fields) for user in users
            ]

    @strawberry.field
    async def get_rofl(self) -> bool:
        return True
