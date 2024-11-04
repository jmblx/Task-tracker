from typing import Any

from domain.entities.group.models import Group
from domain.services.group.group_interface import GroupServiceInterface


class DeleteAndReadGroupUseCase:
    def __init__(
        self,
        group_service: GroupServiceInterface,
    ):
        self.group_service = group_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[Group] | Group:
        groups = await self.group_service.delete_and_fetch(
            search_data, selected_fields, order_by, full_delete
        )
        return groups


class DeleteGroupUseCase:
    def __init__(
        self,
        group_service: GroupServiceInterface,
    ):
        self.group_service = group_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        full_delete: bool,
    ) -> None:
        await self.group_service.delete_by_fields(search_data, full_delete)
