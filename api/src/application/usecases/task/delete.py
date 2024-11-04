from typing import Any

from domain.entities.task.models import Task
from domain.services.auth.auth_service import AuthService
from domain.services.task.task_service_interface import TaskServiceInterface
import logging


class DeleteAndReadTaskUseCase:
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
        full_delete: bool,
    ) -> list[Task] | Task:
        tasks = await self.task_service.delete_and_fetch(search_data, selected_fields, order_by, full_delete)

        return tasks


class DeleteTaskUseCase:
    def __init__(
        self,
        task_service: TaskServiceInterface,
    ):
        self.task_service = task_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        full_delete: bool,
    ) -> None:
        await self.task_service.delete_by_fields(search_data, full_delete)
