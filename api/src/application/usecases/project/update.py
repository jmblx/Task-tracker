from typing import Any
from uuid import UUID

from domain.entities.project.models import Project
from domain.services.project.project_service_interface import ProjectServiceInterface


class UpdateProjectAndReadUseCase:
    def __init__(
        self,
        project_service: ProjectServiceInterface,
    ):
        self.project_service = project_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Project | int]:
        projects = await self.project_service.update_and_fetch(
            search_data, upd_data, selected_fields, order_by
        )
        return projects


class UpdateProjectUseCase:
    def __init__(
        self,
        project_service: ProjectServiceInterface,
    ):
        self.project_service = project_service

    async def __call__(
        self,
        search_data: dict[Any, Any],
        upd_data: dict[Any, dict],
    ) -> None:
        await self.project_service.update_by_fields(search_data, upd_data)
