from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.task.models import Task
from domain.repositories.task.repo import TaskRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class TaskRepositoryImpl(BaseRepositoryImpl[Task], TaskRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)
