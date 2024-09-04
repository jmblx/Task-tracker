from abc import ABC, abstractmethod
from typing import Generic, List, Any
from uuid import UUID

from application.dtos.base import BaseDTO
from infrastructure.repositories.base_repository import T, BaseRepository


class EntityService(ABC, Generic[T]):
    # @abstractmethod
    # async def create(self, entity_data: BaseDTO) -> T:
    #     """Создание сущности"""
    #     pass
    #
    # @abstractmethod
    # async def get_by_id(
    #     self, entity_id: int | UUID,
    #     selected_fields: dict[Any, dict[Any, dict]] | None = None
    # ) -> T:
    #     """Получение сущности по ID"""
    #     pass

    @abstractmethod
    async def create_and_fetch(
        self,
        entity_data: BaseDTO,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        """Создание сущности и получение её данных"""
        pass
