from domain.entities.organization.models import Organization
from domain.services.entity_service import EntityService


class OrganizationServiceInterface(EntityService[Organization]): ...
