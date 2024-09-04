from typing import Generic, Type, Any

from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.base import BaseDTO
from infrastructure.repositories.base_repository import T, BaseRepository


class EntityServiceImpl(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self._base_repo = BaseRepository(model, session)

    async def create_and_fetch(
        self,
        entity_data: BaseDTO,
        selected_fields: dict[Any, dict[Any, dict]] | None = None,
    ) -> T:
        entity_id = await self._base_repo.create(entity_data)

        entity = await self._base_repo.read(entity_id, selected_fields)
        return entity
