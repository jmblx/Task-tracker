from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from domain.entities.group.models import Group
from domain.entities.task.models import Task
from domain.repositories.group.repo import GroupRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class GroupRepositoryImpl(BaseRepositoryImpl[Group], GroupRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Group, session)

    async def _delete_related_data(self, group_id: int):
        """Удаляет связанные данные пользователя."""
        stmt = (
            update(Task).where(Task.group_id == group_id).values(group_id=None)
        )
        await self._session.execute(stmt)

    async def _delete_entities(self, stmt):
        """Удаляет пользователей на основе переданного SQL-запроса."""
        groups = (
            (await self._session.execute(stmt.options(load_only(Group.id))))
            .scalars()
            .all()
        )

        for group in groups:
            await self._delete_related_data(group.id)
        await self._session.flush()
        group_ids = [group.id for group in groups]
        await self._session.execute(
            delete(Group).where(Group.id.in_(group_ids))
        )

        await self._session.commit()

    async def delete_by_ids(self, entity_ids: list[int]):
        """Удаляет пользователей по списку ID."""
        stmt = select(Group).where(Group.id.in_(entity_ids))
        await self._delete_entities(stmt)

    async def delete_by_fields(self, search_data: dict[str, Any]):
        """Удаляет пользователей по полям и значениям, переданным в словаре."""
        stmt = select(Group)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)

        await self._delete_entities(stmt)
