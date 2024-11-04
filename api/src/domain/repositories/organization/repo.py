from abc import ABC

from domain.entities.organization.models import Organization
from domain.repositories.base_repo import BaseRepository


class OrganizationRepository(BaseRepository[Organization], ABC): ...
