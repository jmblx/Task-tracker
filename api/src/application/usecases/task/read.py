from typing import Any
import logging

from domain.entities.task.models import Task
from domain.services.auth.auth_service import AuthService
from domain.services.task.task_service_interface import TaskServiceInterface


class ReadTaskUseCase:
    def __init__(
        self,
        task_service: TaskServiceInterface,
        auth_service: AuthService,
    ):
        self.task_service = task_service
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Task]:
        tasks = await self.task_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        return tasks
