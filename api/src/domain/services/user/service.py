from abc import abstractmethod, ABC
from typing import Any

from domain.entities.user.models import User


class UserServiceInterface(ABC):
    @abstractmethod
    async def create_and_fetch(
        self,
        data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        """Создать пользователя и получить его данные по указанным полям."""
        pass

    @abstractmethod
    async def get_by_id(
        self,
        user_id: int,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        """Получить пользователя по ID и указанным полям."""
        pass

    @abstractmethod
    async def get_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> User:
        """Получить пользователя по заданным параметрам поиска."""
        pass

    @abstractmethod
    async def get_many_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
        order_by: dict[str, str] | None = None,
    ) -> list[User]:
        """Получить список пользователей по заданным параметрам поиска и сортировки."""
        pass

    @abstractmethod
    async def update_by_fields(
        self, search_params: dict[str, Any], upd_data: dict[str, Any]
    ):
        """Обновить данные пользователя по заданным параметрам поиска."""
        pass
