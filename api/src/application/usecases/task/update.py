from typing import Any

from domain.entities.task.models import Task
from domain.services.task.task_service_interface import TaskServiceInterface


class UpdateTaskAndReadUseCase:
    def __init__(
        self,
        task_service: TaskServiceInterface,
    ):
        self.task_service = task_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Task | int]:
        task = await self.task_service.update_and_fetch(
            search_data, upd_data, selected_fields, order_by
        )
        return task


class UpdateTaskUseCase:
    def __init__(
        self,
        task_service: TaskServiceInterface,
    ):
        self._service = task_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
    ) -> None:
        await self.task_service.update_by_fields(search_data, upd_data)
