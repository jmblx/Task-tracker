import json
import logging
from typing import Any

from nats.aio.client import Client

from core.db.database import Base
from core.db.utils import default_update
from core.di.container import container

logger = logging.getLogger(__name__)


async def send_via_nats(
    nats_client: Client,
    subject: str,
    json_message: str | None = None,
    data: dict | None = None,
    string: str | None = None,
):
    if json_message:
        await nats_client.publish(subject, json_message.encode("utf-8"))
    elif data:
        await nats_client.publish(subject, json.dumps(data).encode("utf-8"))
    elif string:
        await nats_client.publish(subject, string.encode("utf-8"))


async def process_notifications(
    data: dict,
    notify_from_data_kwargs: dict[str, str] | None,
    notify_kwargs: dict[str, str] | None,
    notify_subject: str | None,
    model_class: Base,
    obj_id: Any,
    *,
    need_update: bool,
) -> None:
    if notify_from_data_kwargs is not None:
        notify_kwargs.update(
            {
                k: data.__dict__[v]
                for k, v in notify_from_data_kwargs.items()
                if v in data.__dict__
            }
        )

    async with container() as ioc:
        nats_client = await ioc.get(Client)

        await send_via_nats(
            nats_client=nats_client,
            subject=notify_subject,
            data=notify_kwargs,
        )

    if need_update:
        await default_update(model_class, obj_id, notify_kwargs)
