from domain.entities.role.models import Role
from domain.repositories.role.repo import RoleRepository
from domain.services.role.role_service_interface import RoleServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class RoleServiceImpl(EntityServiceImpl[Role], RoleServiceInterface):
    def __init__(self, base_repo: RoleRepository):
        super().__init__(base_repo)
