from domain.entities.role.models import Role
from domain.services.entity_service import EntityService


class RoleServiceInterface(EntityService[Role]): ...
