from dataclasses import asdict
from typing import Any, Annotated, TypeVar, Generic, Type
from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.base import BaseDTO
from core.db.database import Base
from core.utils import create_query_options


# Создаем generic тип для модели
T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self._model = model
        self._session = session

    async def create(
        self, data: BaseDTO
    ) -> int | UUID:
        entitiy_id = (await self._session.execute(
            insert(self._model).values(
                asdict(data)
            ).returning(self._model.id)
        )).scalar()
        await self._session.commit()
        return entitiy_id

    async def read(self, obj_id: int | UUID, selected_fields: dict[Any, dict[Any, dict]]) -> BaseDTO:
        if selected_fields:
            # selected_fields = extract_selected_fields(
            #     info, snake_to_camel(function_name)
            # )                                                                            это в юзкейс откуда это будет вызываться
            # normalized_operations = to_snake_case(selected_fields)
            # selected_fields = normalized_operations.get(function_name, {})
            query_options = create_query_options(self._model, selected_fields)
            query = select(self._model)
            for option in query_options or []:
                query = query.options(option)
            entity = (
                (await self._session.execute(query.where(self._model.id == obj_id)))
                .unique()
                .scalar()
            )
            return entity
        return await self._session.get(self._model, obj_id)

    async def update(self, obj_id: int | UUID, data: BaseDTO) -> bool:
        self._session.execute(update(self._model, obj_id).values(**asdict(data)))
        self._session.commit()
        return True

    async def delete(self, obj_id: int | UUID) -> bool:
        await self._session.execute(
            delete(self._model).where(self._model == obj_id)
        )
        self._session.commit()
        return True

    async def all(
            self,
            params: Annotated[dict[Any, Any], "параметры для поиска"],
            selected_fields: dict[Any, dict[Any, dict]]
    ) -> list[BaseDTO]:

        # selected_fields = extract_selected_fields(
        #     info, snake_to_camel(function_name)
        # )                                                                            это в юзкейс откуда это будет вызываться
        # normalized_operations = to_snake_case(selected_fields)
        # selected_fields = normalized_operations.get(function_name, {})
        query = select(self._model)
        if selected_fields:
            query_options = create_query_options(self._model, selected_fields)
            for option in query_options or []:
                query = query.options(option)
        for key, value in params.items():
            if value is not None:
                query = query.where(getattr(self, key) == value)

        entities = (
            (await self._session.execute(query))
        ).scalars()
        return entities
