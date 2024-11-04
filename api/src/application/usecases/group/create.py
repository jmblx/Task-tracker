from typing import Any

from domain.entities.group.models import Group
from domain.services.group.group_interface import GroupServiceInterface
from domain.services.group.validation import GroupValidationService


class CreateGroupAndReadUseCase:
    def __init__(
        self,
        group_service: GroupServiceInterface,
        validation_service: GroupValidationService,
    ):
        self.group_service = group_service
        self.validation_service = validation_service

    async def __call__(
        self,
        group_data: dict,
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> Group:
        self.validation_service.validate_create_data(group_data)
        groups = await self.group_service.create_and_fetch(
            group_data, selected_fields
        )
        return groups
