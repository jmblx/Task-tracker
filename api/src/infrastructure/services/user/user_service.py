
from domain.entities.user.models import User
from domain.repositories.user.repo import UserRepository
from domain.services.user.user_service_interface import UserServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class UserServiceImpl(EntityServiceImpl[User], UserServiceInterface):
    def __init__(self, base_repo: UserRepository):
        super().__init__(base_repo)
