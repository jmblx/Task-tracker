from typing import Any

from domain.services.user.service import UserServiceInterface
from infrastructure.services.user.service_impl import UserServiceImpl
from presentation.gql.user.types import UserType


class ReadUserUseCase:
    def __init__(
        self,
        user_service: UserServiceInterface,
    ):
        self.user_service = user_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[UserType]:
        users = await self.user_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        return users
