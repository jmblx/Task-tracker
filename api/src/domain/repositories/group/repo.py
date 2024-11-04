from abc import ABC

from domain.entities.group.models import Group
from domain.repositories.base_repo import BaseRepository


class GroupRepository(BaseRepository[Group], ABC): ...
