from typing import Any
from uuid import UUID
import logging

from domain.entities.user.models import User
from domain.services.auth.auth_service import AuthService
from domain.services.user.access_policy import UserAccessPolicyInterface
from domain.services.user.user_service_interface import UserServiceInterface


class UpdateUserAndReadUseCase:
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
        upd_data: dict[Any, dict],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[User | int | UUID]:
        required_data_requester, required_data_user, checks = await self.access_policy.get_required_data("update", upd_data)

        requester = await self.auth_service.get_user_by_token(auth_token, required_data_requester.get("user"))

        target_users = await self.user_service.get_many_by_fields(search_data, required_data_user)
        for target_user in target_users:
            target_user_data = {"user": {}}
            for field in required_data_user["user"]:
                if hasattr(target_user, field):
                    target_user_data["user"][field] = getattr(target_user, field)
            if not await self.access_policy.check_access(requester, target_user_data, checks):
                logging.warning(f"Access denied for user {requester.id} to user {target_user.id}")
                raise PermissionError(f"Access denied to user {target_user.id}")

        await self.user_service.update_by_fields(search_data, upd_data)

        updated_users = await self.user_service.get_many_by_fields(search_data, selected_fields, order_by)

        return updated_users

# UseCase для обновления пользователя
class UpdateUserUseCase:
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
        upd_data: dict[Any, dict],
    ) -> None:
        required_data_requester, required_data_user, checks = await self.access_policy.get_required_data("update", upd_data)

        requester = await self.auth_service.get_user_by_token(auth_token, required_data_requester.get("user"))

        target_users = await self.user_service.get_many_by_fields(search_data, required_data_user)
        for target_user in target_users:
            target_user_data = {"user": {}}
            for field in required_data_user["user"]:
                if hasattr(target_user, field):
                    target_user_data["user"][field] = getattr(target_user, field)
            if not await self.access_policy.check_access(requester, target_user_data, checks):
                logging.warning(f"Access denied for user {requester.id} to user {target_user.id}")
                raise PermissionError(f"Access denied to user {target_user.id}")

        await self.user_service.update_by_fields(search_data, upd_data)
