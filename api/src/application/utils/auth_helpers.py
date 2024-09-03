import logging
from typing import TYPE_CHECKING

import asyncpg
from fastapi import HTTPException
from redis.asyncio import Redis

from application.utils.helpers import create_access_token
from application.utils.jwt_utils import decode_jwt, validate_password
from core.db.utils import get_user_by_id
from core.di.container import container
from domain.entities.user.models import User
from infrastructure.repositories.user.crud import get_user_by_email

if TYPE_CHECKING:
    from config import AuthJWT


async def auth_user(email: str, password: str | None = None) -> User:
    try:
        user = await get_user_by_email(email)
    except asyncpg.exceptions.InterfaceError as e:
        print(e)
    if password and user and validate_password(password, user.hashed_password):
        return user
    elif user and not password:
        return user
    raise HTTPException(status_code=401)


logger = logging.getLogger(__name__)


async def refresh_access_token(refresh_token: str, fingerprint: str) -> str:

    async with container() as ioc:
        redis = await ioc.get(Redis)
        auth_settings = await ioc.get(AuthJWT)
        payload = decode_jwt(refresh_token, auth_settings)
        jti = payload.get("jti")
        token_data = await redis.hgetall(f"refresh_token:{jti}")

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_data.get("fingerprint") != fingerprint:
        raise HTTPException(status_code=401, detail="Invalid fingerprint")

    user = await get_user_by_id(payload.get("sub"))

    access_token = create_access_token(user, auth_settings)

    return access_token
