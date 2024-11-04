from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.project.models import Organization
from domain.repositories.organization.repo import OrganizationRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class OrganizationRepositoryImpl(BaseRepositoryImpl[Organization], OrganizationRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)
