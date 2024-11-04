import logging
from collections.abc import Sequence
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import (
    Row,
    RowMapping,
    asc,
    delete,
    desc,
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import Base
from core.utils import create_query_options
from domain.repositories.base_repo import BaseRepository

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
            if value is not None and isinstance(value, list):
                query = query.where(getattr(self._model, key).in_(value))
            elif value is not None:
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

    async def update_by_fields(
        self,
        search_data: dict[str, Any],
        upd_data: dict[str, Any],
        return_id: bool = True,
    ) -> Sequence[Row | RowMapping | Any] | None:
        stmt = update(self._model)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)
        stmt = stmt.values(**upd_data)
        if return_id:
            entities_ids = await self._session.execute(
                stmt.returning(self._model.id)
            )
            await self._session.commit()
            return entities_ids.scalars().all()
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_by_fields(self, search_data: dict[str, Any]) -> bool:
        stmt = delete(self._model)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)
        result = await self._session.execute(stmt)
        await self._session.commit()

        if result.rowcount == 0:
            raise ValueError("Object not found for deletion.")

        logging.info(result.rowcount)
        return True

    async def soft_delete_by_fields(self, search_data: dict[str, Any]) -> bool:
        stmt = update(self._model)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)
        stmt = stmt.values(is_active=False)
        result = await self._session.execute(stmt)
        await self._session.commit()
        logging.info(result.rowcount)
        if result.rowcount == 0:
            raise ValueError("Object not found for soft deletion.")
        return True

    async def delete_by_ids(self, entity_ids: list[int]):
        stmt = delete(self._model)
        stmt = stmt.where(self._model.id.in_(entity_ids))
        result = await self._session.execute(stmt)
        await self._session.commit()

        if result.rowcount == 0:
            raise ValueError("Object not found for soft deletion.")
        return True

    async def soft_delete_by_ids(self, entity_ids: list[int]):
        stmt = update(self._model)
        print(entity_ids, "aaa")
        stmt = stmt.where(self._model.id.in_(entity_ids)).values(
            is_active=False
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        if result.rowcount == 0:
            raise ValueError("Object not found for soft deletion.")
        return True
