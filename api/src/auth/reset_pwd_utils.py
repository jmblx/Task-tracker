import secrets
from typing import TYPE_CHECKING

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt_utils import hash_password
from auth.models import User
from deps.cont import container
from message_routing.nats_utils import send_via_nats

if TYPE_CHECKING:
    from nats.aio.client import Client


async def set_new_pwd(user: User, new_pwd):
    async with container() as di:
        session = await di.get(AsyncSession)
        hashed_pwd = hash_password(new_pwd)
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(hashed_password=hashed_pwd)
        )
        await session.execute(stmt)
        await session.commit()


async def send_request_change_password(
    user_email: str, nats_client: "Client"
) -> str:
    token: str = secrets.token_urlsafe(32)
    await send_via_nats(
        nats_client=nats_client,
        subject="email.reset_password",
        data={"token": token, "email": user_email},
    )
    return token
