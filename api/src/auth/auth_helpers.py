from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.crud import get_user_by_email
from auth.helpers import create_access_token
from auth.jwt_utils import decode_jwt, validate_password
from auth.models import User
from db.utils import get_user_by_id
from myredis.redis_config import get_redis


async def auth_user(email: str, password: str | None = None) -> User:
    user = await get_user_by_email(email)
    if password and user and validate_password(password, user.hashed_password):
        return user
    elif user and not password:
        return user
    raise HTTPException(status_code=401)


async def refresh_access_token(
    session: AsyncSession, refresh_token: str, fingerprint: str
) -> str:
    payload = decode_jwt(refresh_token)
    jti = payload.get("jti")

    async with get_redis() as redis:
        token_data = await redis.hgetall(f"refresh_token:{jti}")
        if not token_data:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token"
            )

        if token_data.get("fingerprint") != fingerprint:
            raise HTTPException(status_code=401, detail="Invalid fingerprint")

        user = await get_user_by_id(payload.get("sub"))
        return create_access_token(user)
