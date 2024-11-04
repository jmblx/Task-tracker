from typing import Any

from domain.entities.group.models import Group
from domain.services.group.group_interface import GroupServiceInterface


class ReadGroupUseCase:
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
    ) -> list[Group]:
        groups = await self.group_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        return groups
