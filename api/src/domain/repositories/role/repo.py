from abc import ABC

from domain.entities.role.models import Role
from domain.repositories.base_repo import BaseRepository


class RoleRepository(BaseRepository[Role], ABC): ...
