from typing import Any
from uuid import UUID

from domain.entities.role.models import Role
from domain.services.role.role_service_interface import RoleServiceInterface


class UpdateRoleAndReadUseCase:
    def __init__(
        self,
        role_service: RoleServiceInterface,
    ):
        self.role_service = role_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Role | int]:
        role = await self.role_service.update_and_fetch(
            search_data, upd_data, selected_fields, order_by
        )
        return role


class UpdateRoleUseCase:
    def __init__(
        self,
        role_service: RoleServiceInterface,
    ):
        self.role_service = role_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
    ) -> None:
        await self.role_service.update_by_fields(search_data, upd_data)
