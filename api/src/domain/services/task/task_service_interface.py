from domain.entities.task.models import Task
from domain.services.entity_service import EntityService


class TaskServiceInterface(EntityService[Task]): ...
