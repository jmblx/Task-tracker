from aiodataloader import DataLoader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from sqlalchemy.orm import selectinload

from auth.models import User, Role
from task.models import Task


class Loader(DataLoader):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__()


class UserLoader(Loader):

    async def batch_load_fn(self, keys: List[int]):
        users = await self.session.execute(select(User).filter(User.id.in_(keys)))
        user_map = {user.id: user for user in users.unique().scalars().all()}
        return [user_map.get(key) for key in keys]


class RoleLoader(Loader):

    async def batch_load_fn(self, keys: List[int]):
        roles = await self.session.execute(select(Role).filter(Role.id.in_(keys)))
        role_map = {role.id: role for role in roles.scalars().all()}
        return [role_map.get(key) for key in keys]


class TaskLoader(Loader):

    async def batch_load_fn(self, keys: List[int]):
        tasks = await self.session.execute(
            select(Task)
            .join(Task.assignees)
            .filter(User.id.in_(keys))
            .options(selectinload(Task.assignees))
        )

        task_map = {}
        for task in tasks.unique().scalars().all():
            for user in task.assignees:
                if user.id not in task_map:
                    task_map[user.id] = []
                task_map[user.id].append(task)

        return [task_map.get(key, []) for key in keys]


class TaskCreatedLoader(Loader):

    async def batch_load_fn(self, keys: List[int]):
        # Выполнение запроса на выборку задач, связанных с пользователями через таблицу user_task
        tasks = await self.session.execute(
            select(Task)
            .join(Task.assignees)
            .filter(User.id.in_(keys))
            .options(selectinload(Task.assignees))
        )

        # Создание словаря задач, связанных с пользователями
        task_map = {}
        for task in tasks.scalars().all():
            for user in task.assignees:
                if user.id not in task_map:
                    task_map[user.id] = []
                task_map[user.id].append(task)

        return [task_map.get(key, []) for key in keys]
