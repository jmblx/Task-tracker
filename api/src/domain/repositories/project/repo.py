from abc import ABC

from domain.entities.project.models import Project
from domain.repositories.base_repo import BaseRepository


class ProjectRepository(BaseRepository[Project], ABC): ...
