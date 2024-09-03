from dataclasses import asdict
import secrets

from nats.aio.client import Client

from application.dtos.user import UserCreateDTO
from core.db.utils import get_selected_fields
from core.utils import hash_user_pwd
from domain.services.user.service import UserService
from infrastructure.external_services.message_routing.nats_utils import send_via_nats
from infrastructure.external_services.message_routing.notify_service import NotifyService


class CreateUserAndReadUseCase:
    def __init__(self, user_service: UserService, notify_service: NotifyService):
        self.user_service = user_service
        self.notify_service = notify_service

    async def execute(self, user_data: UserCreateDTO, info):  # Пароль уже хэшированный и т.д.
        selected_fields = get_selected_fields(info, 'user')

        email_confirmation_token = secrets.token_urlsafe(32)
        user_data.email_confirmation_token = email_confirmation_token

        user = await self.user_service.create_and_fetch(user_data, selected_fields)

        notify_data = {
            "email_confirmation_token": email_confirmation_token,
            "email": user.email
        }
        await self.notify_service.email_register_notify(data=notify_data)

        return user
