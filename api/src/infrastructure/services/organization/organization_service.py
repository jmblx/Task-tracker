from domain.entities.organization.models import Organization
from domain.repositories.organization.repo import OrganizationRepository
from domain.services.organization.organization_service_interface import OrganizationServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class OrganizationServiceImpl(EntityServiceImpl[Organization], OrganizationServiceInterface):
    def __init__(self, base_repo: OrganizationRepository):
        super().__init__(base_repo)
