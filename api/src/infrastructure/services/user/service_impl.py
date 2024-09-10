from typing import Any

from domain.entities.user.models import User
from domain.services.entity_service import EntityService
from domain.services.user.service import UserServiceInterface


class UserServiceImpl(UserServiceInterface):
    def __init__(self, entity_service: UserServiceInterface):
        self._entity_service = entity_service

    async def create_and_fetch(
        self,
        data: dict,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        user = await self._entity_service.create_and_fetch(
            data, selected_fields
        )
        return user

    async def get_by_id(
        self,
        user_id: int,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        user = await self._entity_service.get_by_id(user_id, selected_fields)
        return user

    async def get_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        user = await self._entity_service.get_by_fields(
            search_params, selected_fields
        )
        return user

    async def get_many_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
        order_by: dict[str, str] | None = None,
    ) -> list[User]:
        users = await self._entity_service.get_many_by_fields(
            search_params, selected_fields, order_by
        )
        return users

    async def update_by_fields(
        self, search_params: dict[str, Any], upd_data: dict[str, Any]
    ):
        await self._entity_service.update_by_fields(search_params, upd_data)

    # async def delete_by_fields(self, search_params: dict[str, Any]):
    #     await self._entity_service.delete_by_fields(search_params)
