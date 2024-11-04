from typing import Any
from uuid import UUID

from domain.entities.group.models import Group
from domain.services.group.group_interface import GroupServiceInterface


class UpdateGroupAndReadUseCase:
    def __init__(
        self,
        group_service: GroupServiceInterface,
    ):
        self.group_service = group_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Group | int | UUID]:
        groups = await self.group_service.update_and_fetch(
            search_data, upd_data, selected_fields, order_by
        )
        return groups


class UpdateGroupUseCase:
    def __init__(
        self,
        group_service: GroupServiceInterface,
    ):
        self.group_service = group_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
    ) -> None:
        await self.group_service.update_by_fields(search_data, upd_data)
