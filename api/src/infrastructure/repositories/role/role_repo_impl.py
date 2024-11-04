from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.role.models import Role
from domain.repositories.role.repo import RoleRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class RoleRepositoryImpl(BaseRepositoryImpl[Role], RoleRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)
