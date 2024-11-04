import secrets

from nats.aio.client import Client

from domain.services.notification.service import NotifyService
from infrastructure.external_services.message_routing.nats_utils import (
    send_via_nats,
)


class NotifyServiceImpl(NotifyService):
    def __init__(self, nats_client: Client):
        self._nats_client = nats_client

    async def email_register_notify(self, data: dict) -> None:
        await send_via_nats(self._nats_client, "email.confirmation", data=data)

    async def pwd_reset_notify(self, user_email: str) -> str:
        token: str = secrets.token_urlsafe(32)
        await send_via_nats(
            nats_client=self._nats_client,
            subject="email.reset_password",
            data={"token": token, "email": user_email},
        )
        return token
