import logging
from typing import Any
from domain.entities.project.models import Project
from domain.services.auth.auth_service import AuthService
from domain.services.project.access_policy import ProjectAccessPolicyInterface
from domain.services.project.project_service_interface import ProjectServiceInterface


class CreateProjectAndReadUseCase:
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
        project_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
    ) -> Project:
        (
            required_data_requester,
            required_data_project,
            checks,
        ) = await self.access_policy.get_required_data("create", project_data)

        requester = await self.auth_service.get_user_by_token(
            auth_token, required_data_requester.get("user")
        )

        target_data = {"project": {}}
        for field in required_data_project.get("project", {}):
            if field in project_data:
                target_data["project"][field] = project_data[field]
            else:
                raise ValueError(f"Missing required field {field} in project_data")

        if not await self.access_policy.check_access(requester, target_data, checks):
            logging.warning(
                f"Access denied for user {requester.id} to create project"
            )
            raise PermissionError("Access denied to create project")

        project = await self.project_service.create_and_fetch(
            project_data, selected_fields
        )
        return project
