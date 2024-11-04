from typing import Any

from domain.entities.project.models import Project
from domain.services.auth.auth_service import AuthService
from domain.services.project.project_service_interface import ProjectServiceInterface
import logging


class DeleteAndReadProjectUseCase:
    def __init__(
        self,
        project_service: ProjectServiceInterface,
        auth_service: AuthService,
    ):
        self.project_service = project_service
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[Project] | Project:
        projects = await self.project_service.delete_and_fetch(search_data, selected_fields, order_by, full_delete)

        return projects


class DeleteProjectUseCase:
    def __init__(
        self,
        project_service: ProjectServiceInterface,
    ):
        self.project_service = project_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        full_delete: bool,
    ) -> None:
        await self.project_service.delete_by_fields(search_data, full_delete)
