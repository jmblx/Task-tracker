import logging
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlalchemy.sql import Select

from core.exceptions.user.delete import UserIsAdminOfOrgsException
from domain.entities.group.models import Group
from domain.entities.organization.models import UserOrg
from domain.entities.task.models import UserTask
from domain.entities.user.models import User
from domain.repositories.user.repo import UserRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class UserRepositoryImpl(BaseRepositoryImpl[User], UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def delete_related_data(self, user_id: int):
        """Удаляет связанные данные пользователя."""
        orgs = (
            (
                await self._session.execute(
                    select(UserOrg).where(UserOrg.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        users_org = [org.id for org in orgs if "admin" in org.permissions]
        if users_org:
            raise UserIsAdminOfOrgsException(users_org)

        await self._session.execute(
            delete(UserTask).where(UserTask.user_id == user_id)
        )

        groups = (
            (
                await self._session.execute(
                    select(Group).where(Group.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        project_groups, user_groups = [], []
        for group in groups:
            if group.project_id is not None:
                project_groups.append(group.id)
            else:
                user_groups.append(group.id)

        await self._session.execute(
            delete(Group).where(Group.id.in_(user_groups))
        )
        await self._session.execute(
            update(Group)
            .where(Group.id.in_(project_groups))
            .values(user_id=None)
        )

    async def delete_entities(self, stmt: Select):
        """Удаляет пользователей на основе переданного SQL-запроса."""
        users = (
            (await self._session.execute(stmt.options(load_only(User.id))))
            .scalars()
            .all()
        )
        if not users:
            raise ValueError("Object not found for deletion.")
        for user in users:
            await self.delete_related_data(user.id)
            result = await self._session.execute(delete(User).where(User.id == user.id))
            logging.info(result.rowcount)

        await self._session.commit()

    async def delete_by_ids(self, entity_ids: list[int]):
        """Удаляет пользователей по списку ID."""
        stmt = select(User).where(User.id.in_(entity_ids))
        await self.delete_entities(stmt)

    async def delete_by_fields(self, search_data: dict[str, Any]):
        """Удаляет пользователей по полям и значениям, переданным в словаре."""
        stmt = select(User)
        for key, value in search_data.items():
            if value is not None:
                stmt = stmt.where(getattr(self._model, key) == value)
        await self.delete_entities(stmt)
