import logging
from typing import Any, List

from domain.entities.user.models import User
from domain.services.auth.auth_service import AuthService
from domain.services.user.user_service_interface import UserServiceInterface
from domain.services.user.access_policy import UserAccessPolicyInterface


class ReadUserUseCase:
    def __init__(
        self,
        user_service: UserServiceInterface,
        access_policy: UserAccessPolicyInterface,
        auth_service: AuthService,
    ):
        self.user_service = user_service
        self.access_policy = access_policy
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> List[User]:
        _, required_data_user, checks = await self.access_policy.get_required_data("read", selected_fields)

        requester = await self.auth_service.get_user_by_token(auth_token, required_data_user.get("user"))

        target_users = await self.user_service.get_many_by_fields(
            search_data, required_data_user.get("user")
        )
        for target_user in target_users:
            target_user_data = {"user": {}}
            for field in required_data_user["user"]:
                if hasattr(target_user, field):
                    target_user_data["user"][field] = getattr(target_user, field)
            if not await self.access_policy.check_access(requester, target_user_data, checks):
                logging.warning(f"Access denied for user {requester.id} to user {target_user.id}")
                raise PermissionError(f"Access denied to user {target_user.id}")

        users = await self.user_service.get_many_by_fields(
            search_data, selected_fields, order_by
        )

        return users

