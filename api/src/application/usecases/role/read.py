from typing import Any
import logging

from domain.entities.role.models import Role
from domain.services.auth.auth_service import AuthService
from domain.services.role.role_service_interface import RoleServiceInterface


class ReadRoleUseCase:
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
    ) -> list[Role]:
        roles = await self.role_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        return roles
