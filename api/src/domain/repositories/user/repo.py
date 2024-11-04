from abc import ABC

from domain.entities.user.models import User
from domain.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User], ABC): ...
