from application.dtos.user import UserCreateDTO
from core.utils import hash_user_pwd
from domain.entities.user.models import User
from domain.services.entity_service import EntityService


class UserService(EntityService[User]):
    def __init__(self, base_service: EntityService):
        self._base_service = base_service

    async def create_and_fetch(self, data: UserCreateDTO):

        pwd = self.__dict__.pop("password", None)
        if pwd:
            # Хэшируем пароль и сохраняем в hashed_password
            self.hashed_password = hash_user_pwd(user_id, pwd)
