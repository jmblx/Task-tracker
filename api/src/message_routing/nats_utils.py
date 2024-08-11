import json
from typing import Optional, Dict, Any

from nats.aio.client import Client as NATS
from strawberry import Info

from db.database import Base
from db.utils import default_update


async def send_via_nats(
    nats_client: NATS,
    subject: str,
    json_message: str = None,
    data: dict = None,
    string: str = None,
):
    if json_message:
        await nats_client.publish(subject, json_message.encode("utf-8"))
    elif data:
        await nats_client.publish(subject, json.dumps(data).encode("utf-8"))
    elif string:
        await nats_client.publish(subject, string.encode("utf-8"))


async def process_notifications(
    info: Info,
    data: dict,
    notify_from_data_kwargs: Optional[Dict[str, str]],
    notify_kwargs: Optional[Dict[str, str]],
    notify_subject: Optional[str],
    model_class: Base,
    obj_id: Any,
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

        nats_client = info.context["nats_client"]
        await send_via_nats(
            nats_client=nats_client,
            subject=notify_subject,
            data=notify_kwargs,
        )

        if need_update:
            await default_update(model_class, obj_id, notify_kwargs)
