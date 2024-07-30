from fastapi import HTTPException

from auth.crud import get_user_by_email, get_user_by_id
from auth.helpers import create_access_token
from auth.models import User
from auth.utils import validate_password, decode_jwt
from myredis.redis_config import get_redis


async def authenticate_user(email: str, password: str) -> User:
    user = await get_user_by_email(email)
    if user and validate_password(password, user.hashed_password):
        return user
    raise HTTPException(status_code=401)


async def refresh_access_token(refresh_token: str, fingerprint: str) -> str:
    payload = decode_jwt(refresh_token)
    jti = payload.get("jti")

    async with get_redis() as redis:
        token_data = await redis.hgetall(f"refresh_token:{jti}")
        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        if token_data.get("fingerprint") != fingerprint:
            raise HTTPException(status_code=401, detail="Invalid fingerprint")

        user = await get_user_by_id(payload.get("sub"))
        return create_access_token(user)
