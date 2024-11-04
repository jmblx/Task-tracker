from typing import Any

from domain.entities.organization.models import Organization
from domain.services.auth.auth_service import AuthService
from domain.services.organization.organization_service_interface import OrganizationServiceInterface


class ReadOrganizationUseCase:
    def __init__(
        self,
        organization_service: OrganizationServiceInterface,
        auth_service: AuthService,
    ):
        self.organization_service = organization_service
        self.auth_service = auth_service

    async def __call__(
        self,
        # auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Organization]:
        organizations = await self.organization_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        return organizations
