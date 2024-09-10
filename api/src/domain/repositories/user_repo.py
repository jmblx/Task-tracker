from abc import ABC, abstractmethod
from typing import Generic, Any, TypeVar
from uuid import UUID

from core.db.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> int | UUID:
        """Создает новую запись в базе данных."""
        pass

    @abstractmethod
    async def get_by_fields(
        self,
        search_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> T:
        """Получает одну запись по указанным критериям."""
        pass

    @abstractmethod
    async def get_many_by_fields(
        self,
        search_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict[str, str] | None = None,
    ) -> list[T]:
        """Получает несколько записей по указанным критериям с возможностью сортировки."""
        pass

    @abstractmethod
    async def update_many_by_fields(
        self, search_data: dict[str, Any], upd_data: dict[str, Any]
    ) -> bool:
        """Обновляет записи по указанным критериям."""
        pass

    # @abstractmethod
    # async def delete(self, search_data: dict[str, Any]) -> bool:
    #     """Удаляет записи по указанным критериям."""
    #     pass
