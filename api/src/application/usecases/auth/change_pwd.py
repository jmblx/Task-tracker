from datetime import timedelta
from uuid import UUID

from redis.asyncio import Redis

from domain.services.auth.reset_pwd_service import ResetPwdService
from domain.services.user.service import UserServiceInterface
from infrastructure.services.user.service_impl import UserServiceImpl
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)
from infrastructure.services.auth.reset_pwd_service import ResetPwdServiceImpl


class RequestChangePasswordUseCase:
    def __init__(
        self,
        notify_service: NotifyServiceImpl,
        user_service: UserServiceInterface,
        reset_pwd_service: ResetPwdService,
    ):
        self.notify_service = notify_service
        self.user_service = user_service
        self.reset_pwd_service = reset_pwd_service

    async def __call__(
        self, email: str | None = None, full_name: dict[str, str] | None = None
    ) -> bool:
        if email:
            selected_fields = {"id": {}}
            search_data = {"email": email}
        else:
            selected_fields = {"id": {}, "first_name": {}, "last_name": {}}
            search_data = {
                "first_name": full_name["first_name"],
                "last_name": full_name["last_name"],
            }
        user = await self.user_service.get_by_fields(
            search_data, selected_fields
        )
        email = user.email if not email else email

        token = await self.notify_service.pwd_reset_notify(email)

        await self.reset_pwd_service.save_password_reset_token(user.id, token)
        return True
