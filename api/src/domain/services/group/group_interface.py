from domain.entities.group.models import Group
from domain.services.entity_service import EntityService


class GroupServiceInterface(EntityService[Group]): ...
