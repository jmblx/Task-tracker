import secrets

from application.dtos.user import UserCreateDTO
from core.db.utils import get_selected_fields
from domain.services.user.service import UserService
from domain.services.user.validation import ValidationService
from infrastructure.external_services.message_routing.notify_service import (
    NotifyService,
)
from domain.services.security.pwd_service import HashService
from presentation.gql.user.types import UserType


class CreateUserAndReadUseCase:
    def __init__(
        self,
        user_service: UserService,
        notify_service: NotifyService,
        hash_service: HashService,
        validation_service: ValidationService,
    ):
        self.user_service = user_service
        self.notify_service = notify_service
        self.hash_service = hash_service
        self.validation_service = validation_service

    async def __call__(self, user_data: UserCreateDTO, info):
        pwd = user_data.__dict__.pop("password", None)
        if pwd:
            user_data.hashed_password = self.hash_service.hash_password(pwd)
        selected_fields = get_selected_fields(info, "addUser")

        email_confirmation_token = secrets.token_urlsafe(32)
        user_data.email_confirmation_token = email_confirmation_token

        user = await self.user_service.create_and_fetch(
            user_data, selected_fields
        )

        notify_data = {
            "email_confirmation_token": email_confirmation_token,
            "email": user.email,
        }
        await self.notify_service.email_register_notify(data=notify_data)

        return UserType.from_instance(user, selected_fields)
