from nats.aio.client import Client

from domain.services.notification.service import NotifyService
from infrastructure.external_services.message_routing.nats_utils import send_via_nats


class NotifyServiceImpl(NotifyService):
    def __init__(self, nats_client: Client):
        self.nats_client = nats_client

    def email_register_notify(self, data: dict):
        await send_via_nats(
            self.nats_client,
            "email.confirmation",
            data=data
        )
