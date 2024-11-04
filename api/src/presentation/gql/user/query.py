import logging

import strawberry
from strawberry import Info

from application.usecases.user.read import ReadUserUseCase
from core.db.utils import get_selected_fields
from core.di.container import container
from core.utils import (
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
        auth_token = info.context.get("auth_token")
        async with container() as ioc:
            interactor = await ioc.get(ReadUserUseCase)
            selected_fields = get_selected_fields(info, "getUser")
            logging.info(selected_fields)
            users = await interactor(
                auth_token, search_data.__dict__, selected_fields, order_by
            )
            return [
                UserType.from_instance(user, selected_fields) for user in users
            ]
