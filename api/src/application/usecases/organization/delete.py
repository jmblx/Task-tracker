from typing import Any

from domain.entities.organization.models import Organization
from domain.services.auth.auth_service import AuthService
from domain.services.organization.organization_service_interface import OrganizationServiceInterface
import logging


class DeleteAndReadOrganizationUseCase:
    def __init__(
        self,
        organization_service: OrganizationServiceInterface,
        auth_service: AuthService,
    ):
        self.organization_service = organization_service
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[Organization] | Organization:
        organizations = await self.organization_service.delete_and_fetch(search_data, selected_fields, order_by, full_delete)

        return organizations


class DeleteOrganizationUseCase:
    def __init__(
        self,
        organization_service: OrganizationServiceInterface,
    ):
        self.organization_service = organization_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        full_delete: bool,
    ) -> None:
        await self.organization_service.delete_by_fields(search_data, full_delete)
