from domain.entities.task.models import Task
from domain.repositories.task.repo import TaskRepository
from domain.services.task.task_service_interface import TaskServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class TaskServiceImpl(EntityServiceImpl[Task], TaskServiceInterface):
    def __init__(self, base_repo: TaskRepository):
        super().__init__(base_repo)
