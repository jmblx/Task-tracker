from typing import Any

from domain.entities.role.models import Role
from domain.services.role.role_service_interface import RoleServiceInterface
from domain.services.role.validation import RoleValidationService


class CreateRoleAndReadUseCase:
    def __init__(
        self,
        role_service: RoleServiceInterface,
        validation_service: RoleValidationService,
    ):
        self.role_service = role_service
        self.validation_service = validation_service

    async def __call__(
        self,
        role_data: dict,
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> Role:
        # self.validation_service.validate_create_data(role_data)
        roles = await self.role_service.create_and_fetch(
            role_data, selected_fields
        )
        return roles
