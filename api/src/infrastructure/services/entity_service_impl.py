from typing import Any, Generic
from uuid import UUID

from domain.repositories.base_repo import BaseRepository
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
        self,
        search_params: dict[str, Any],
        upd_data: dict[str, Any],
    ):
        await self._base_repo.update_by_fields(
            search_params, upd_data, return_id=False
        )

    async def update_and_fetch(
        self,
        search_params: dict[str, Any],
        upd_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict[str, str] | None = None,
    ) -> list[T | int | UUID]:
        entities_ids = await self._base_repo.update_by_fields(
            search_params, upd_data, return_id=True
        )
        if "id" in selected_fields and len(selected_fields) == 1:
            return entities_ids
        entities = await self._base_repo.get_many_by_fields(
            {"id": entities_ids}, selected_fields, order_by
        )
        return entities

    async def delete_by_fields(
        self,
        search_data: dict[str, Any],
        full_delete: bool,
    ) -> None:
        if full_delete:
            await self._base_repo.delete_by_fields(search_data)
        else:
            await self._base_repo.soft_delete_by_fields(search_data)

    async def delete_and_fetch(
        self,
        search_data: dict[str, Any],
        selected_fields: dict[str, dict[str | None, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[T]:
        entities = await self._base_repo.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        if full_delete:
            await self._base_repo.delete_by_ids(
                [entity.id for entity in entities]
            )
        else:
            await self._base_repo.soft_delete_by_ids(
                [entity.id for entity in entities]
            )
        return entities
