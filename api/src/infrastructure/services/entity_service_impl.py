from typing import Any, Generic
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.base import BaseDTO
from domain.repositories.user_repo import BaseRepository
from domain.services.entity_service import EntityService
from infrastructure.repositories.base_repository import T


class EntityServiceImpl(EntityService[T], Generic[T]):
    def __init__(self, base_repo: BaseRepository[T]):
        self._base_repo = base_repo

    async def create_and_fetch(
        self,
        entity_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        entity_id = await self._base_repo.create(entity_data)
        if "id" in selected_fields and len(selected_fields) == 1:
            return entity_id
        entity = await self.get_by_id(entity_id, selected_fields)
        return entity

    async def get_by_id(
        self,
        entity_id: int | UUID,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        entity = await self._base_repo.get_by_fields(
            {"id": entity_id}, selected_fields
        )
        return entity

    async def get_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        entity = await self._base_repo.get_by_fields(
            search_params, selected_fields
        )
        return entity

    async def get_many_by_fields(
        self,
        search_params: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
        order_by: dict[str, str] | None = None,
    ) -> list[T]:
        entities = await self._base_repo.get_many_by_fields(
            search_params, selected_fields, order_by
        )
        return entities

    async def update_by_fields(
        self, search_params: dict[str, Any], upd_data: dict[str, Any]
    ):
        await self._base_service.update_by_fields(search_params, upd_data)
