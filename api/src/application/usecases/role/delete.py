from typing import Any

from domain.entities.role.models import Role
from domain.services.auth.auth_service import AuthService
from domain.services.role.role_service_interface import RoleServiceInterface
import logging


class DeleteAndReadRoleUseCase:
    def __init__(
        self,
        role_service: RoleServiceInterface,
        auth_service: AuthService,
    ):
        self.role_service = role_service
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[Role] | Role:
        roles = await self.role_service.delete_and_fetch(search_data, selected_fields, order_by, full_delete)

        return roles


class DeleteRoleUseCase:
    def __init__(
        self,
        role_service: RoleServiceInterface,
    ):
        self.role_service = role_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        full_delete: bool,
    ) -> None:
        await self.role_service.delete_by_fields(search_data, full_delete)
