from abc import ABC
from dataclasses import asdict
from typing import Annotated, Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, insert, select, update, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.base import BaseDTO
from core.db.database import Base
from core.utils import create_query_options
from domain.repositories.user_repo import BaseRepository

# Создаем generic тип для модели
T = TypeVar("T", bound=Base)


class BaseRepositoryImpl(BaseRepository[T], Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession):
        self._model = model
        self._session = session

    async def create(self, data: dict[str, Any]) -> int | UUID:
        entitiy_id = (
            await self._session.execute(
                insert(self._model)
                .values({k: v for k, v in data.items()})
                .returning(self._model.id)
            )
        ).scalar()
        await self._session.commit()
        return entitiy_id

    async def get_by_fields(
        self,
        search_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> T:
        query_options = create_query_options(self._model, selected_fields)
        query = select(self._model)
        for key, value in search_data.items():
            if value is not None:
                query = query.where(getattr(self._model, key) == value)
        for option in query_options or []:
            query = query.options(option)
        entity = (await self._session.execute(query)).unique().scalar()
        return entity

    async def get_many_by_fields(
        self,
        search_data: dict[str, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict[str, str] | None = None,
    ) -> list[T]:
        query_options = create_query_options(self._model, selected_fields)
        query = select(self._model)

        for key, value in search_data.items():
            if value is not None:
                query = query.where(getattr(self._model, key) == value)

        for option in query_options or []:
            query = query.options(option)

        if order_by:
            field = getattr(self._model, order_by.get("field"))
            direction = (
                asc if order_by.get("direction").upper() == "ASC" else desc
            )
            query = query.order_by(direction(field))

        result = await self._session.execute(query)
        entities = result.unique().scalars().all()
        return entities

    async def update_many_by_fields(
        self, search_data: dict[str, Any], upd_data: dict[str, Any]
    ) -> bool:
        stmt = update(self._model)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)
        await self._session.execute(stmt.values(**upd_data))
        await self._session.commit()
        return True

    async def delete(self, search_data: dict[str, Any]) -> bool:
        stmt = delete(self._model)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)
        await self._session.execute(stmt)
        await self._session.commit()
        return True
