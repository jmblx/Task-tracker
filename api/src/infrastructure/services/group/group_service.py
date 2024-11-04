from domain.entities.group.models import Group
from domain.repositories.group.repo import GroupRepository
from domain.services.group.group_interface import GroupServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class GroupServiceImpl(EntityServiceImpl[Group], GroupServiceInterface):
    def __init__(self, base_repo: GroupRepository):
        super().__init__(base_repo)
