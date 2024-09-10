import secrets
from typing import Any

from application.dtos.user import UserCreateDTO
from domain.services.security.pwd_service import HashService
from domain.services.user.service import UserServiceInterface
from infrastructure.services.user.service_impl import UserServiceImpl
from domain.services.user.validation import UserValidationService
from infrastructure.external_services.message_routing.notify_service import (
    NotifyService,
)
from presentation.gql.user.types import UserType


class CreateUserAndReadUseCase:
    def __init__(
        self,
        user_service: UserServiceInterface,
        notify_service: NotifyService,
        hash_service: HashService,
        validation_service: UserValidationService,
    ):
        self.user_service = user_service
        self.notify_service = notify_service
        self.hash_service = hash_service
        self.validation_service = validation_service

    async def __call__(
        self,
        user_data: dict,
        selected_fields: dict[Any, dict[Any, dict]],
    ):
        self.validation_service.validate_create_data(user_data)
        pwd = user_data.get("password")
        if pwd:
            user_data["hashed_password"] = self.hash_service.hash_password(pwd)
            del user_data["password"]

        email_confirmation_token = secrets.token_urlsafe(32)
        user_data["email_confirmation_token"] = email_confirmation_token

        user = await self.user_service.create_and_fetch(
            user_data, selected_fields
        )

        notify_data = {
            "email_confirmation_token": email_confirmation_token,
            "email": user_data.get("email"),
        }
        await self.notify_service.email_register_notify(data=notify_data)

        return user
