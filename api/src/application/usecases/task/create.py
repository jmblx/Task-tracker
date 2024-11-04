from typing import Any

from domain.entities.task.models import Task
from domain.services.task.task_service_interface import TaskServiceInterface
from domain.services.task.validation import TaskValidationService


class CreateTaskAndReadUseCase:
    def __init__(
        self,
        task_service: TaskServiceInterface,
        validation_service: TaskValidationService,
    ):
        self.task_service = task_service
        self.validation_service = validation_service

    async def __call__(
        self,
        task_data: dict,
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> Task:
        # self.validation_service.validate_create_data(task_data)
        tasks = await self.task_service.create_and_fetch(
            task_data, selected_fields
        )
        return tasks
