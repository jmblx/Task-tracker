from typing import Any
import logging

from domain.entities.project.models import Project
from domain.services.auth.auth_service import AuthService
from domain.services.project.access_policy import ProjectAccessPolicyInterface
from domain.services.project.project_service_interface import ProjectServiceInterface


class ReadProjectUseCase:
    def __init__(
        self,
        project_service: ProjectServiceInterface,
        access_policy: ProjectAccessPolicyInterface,
        auth_service: AuthService,
    ):
        self.project_service = project_service
        self.access_policy = access_policy
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[Project]:
        # Получаем необходимые данные и проверки из политики доступа
        required_data_requester, required_data_project, checks = await self.access_policy.get_required_data("read", selected_fields)
        user_data = required_data_requester.get("user")
        requester = await self.auth_service.get_user_by_token(
            auth_token,
            user_data if user_data else {"id": {}}
        )

        # Получаем целевые проекты с необходимыми данными
        target_projects = await self.project_service.get_many_by_fields(search_data, required_data_project)

        for target_project in target_projects:
            target_project_data = {"project": {}}
            for field in required_data_project.get("project", {}):
                if field == "tasks":
                    # Поле tasks берется из project_data, т.к. оно может требовать дополнительных проверок
                    target_project_data["project"]["organization_id"] = target_project.organization_id
                else:
                    if hasattr(target_project, field):
                        target_project_data["project"][field] = getattr(target_project, field)
            if not await self.access_policy.check_access(requester, target_project_data, checks):
                logging.warning(f"Access denied for user {requester.id} to project {target_project.id}")
                raise PermissionError(f"Access denied to project {target_project.id}")

        # Получаем проекты с выбранными полями для возврата
        projects = await self.project_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )

        return projects
