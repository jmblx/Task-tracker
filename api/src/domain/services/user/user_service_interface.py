
from domain.entities.user.models import User
from domain.services.entity_service import EntityService


class UserServiceInterface(EntityService[User]): ...
