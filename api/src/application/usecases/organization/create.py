from typing import Any

from domain.entities.organization.models import Organization
from domain.services.organization.organization_service_interface import OrganizationServiceInterface
from domain.services.organization.validation import OrganizationValidationService


class CreateOrganizationAndReadUseCase:
    def __init__(
        self,
        organization_service: OrganizationServiceInterface,
        validation_service: OrganizationValidationService,
    ):
        self.organization_service = organization_service
        self.validation_service = validation_service

    async def __call__(
        self,
        organization_data: dict,
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> Organization:
       # self.validation_service.validate_create_data(organization_data)
        organizations = await self.organization_service.create_and_fetch(
            organization_data, selected_fields
        )
        return organizations
