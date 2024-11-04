from abc import ABC

from domain.entities.task.models import Task
from domain.repositories.base_repo import BaseRepository


class TaskRepository(BaseRepository[Task], ABC): ...
