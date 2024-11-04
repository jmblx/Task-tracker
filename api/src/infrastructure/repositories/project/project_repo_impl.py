from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.project.models import Project
from domain.repositories.project.repo import ProjectRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class ProjectRepositoryImpl(BaseRepositoryImpl[Project], ProjectRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)
