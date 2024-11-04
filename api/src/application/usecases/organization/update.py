from typing import Any
from uuid import UUID

from domain.entities.organization.models import Organization
from domain.services.organization.organization_service_interface import OrganizationServiceInterface


class UpdateOrganizationAndReadUseCase:
    def __init__(
        self,
        organization_service: OrganizationServiceInterface,
    ):
        self.organization_service = organization_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Organization | int | UUID]:
        organizations = await self.organization_service.update_and_fetch(
            search_data, upd_data, selected_fields, order_by
        )
        return organizations


class UpdateOrganizationUseCase:
    def __init__(
        self,
        organization_service: OrganizationServiceInterface,
    ):
        self.organization_service = organization_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
    ) -> None:
        await self.organization_service.update_by_fields(search_data, upd_data)
