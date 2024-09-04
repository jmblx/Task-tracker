from typing import Any

from application.dtos.user import UserCreateDTO
from application.utils.jwt_utils import hash_password
from core.utils import hash_user_pwd
from domain.entities.user.models import User
from domain.services.entity_service import EntityService


class UserService(EntityService[User]):
    def __init__(self, base_service: EntityService):
        self._base_service = base_service

    async def create_and_fetch(
        self,
        data: UserCreateDTO,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        user = await self._base_service.create_and_fetch(data, selected_fields)
        return user
