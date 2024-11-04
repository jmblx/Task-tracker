from abc import ABC, abstractmethod
from typing import Any, Generic
from uuid import UUID

from infrastructure.repositories.base_repository import T


class EntityService(ABC, Generic[T]):
    # @abstractmethod
    # async def create(self, entity_data: BaseDTO) -> T:
    #     """Создание сущности"""
    #     pass
    #
    @abstractmethod
    async def get_by_id(
        self,
        entity_id: int | UUID,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        """Получение сущности по ID"""

    @abstractmethod
    async def create_and_fetch(
        self,
        entity_data: dict,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        """Создание сущности и получение её данных"""

    @abstractmethod
    async def get_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> T: ...

    @abstractmethod
    async def get_many_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
        order_by: dict[str, str] | None = None,
    ) -> list[T]: ...

    @abstractmethod
    async def update_by_fields(
        self,
        search_params: dict[str, Any],
        upd_data: dict[str, Any],
    ) -> None: ...

    @abstractmethod
    async def update_and_fetch(
        self,
        search_params: dict[str, Any],
        upd_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict[str, str] | None = None,
    ) -> list[T | int | UUID]: ...

    @abstractmethod
    async def delete_by_fields(
        self,
        search_data: dict[str, Any],
        full_delete: bool,
    ) -> None: ...

    @abstractmethod
    async def delete_and_fetch(
        self,
        search_data: dict[str, Any],
        selected_fields: dict[str, dict[str | None, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[T]: ...
