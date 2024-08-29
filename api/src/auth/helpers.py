from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from pytz import timezone
from starlette.responses import Response
from strawberry import Info
from strawberry.scalars import JSON

from auth import jwt_utils as auth_utils
from auth.models import User
from config import settings
from myredis.utils import save_refresh_token_to_redis

TOKEN_TYPE_FIELD = "type"  # noqa: S105
ACCESS_TOKEN_TYPE = "access"  # noqa: S105
REFRESH_TOKEN_TYPE = "refresh"  # noqa: S105


# def create_jwt(
#     token_type: str,
#     token_data: dict,
#     expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
#     expire_timedelta: timedelta | None = None,
# ) -> str:
#     jwt_payload = {TOKEN_TYPE_FIELD: token_type}
#     jwt_payload.update(token_data)
#     return auth_utils.encode_jwt(
#         payload=jwt_payload,
#         expire_minutes=expire_minutes,
#         expire_timedelta=expire_timedelta,
#     )


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> dict:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    tz = timezone("Europe/Moscow")
    now = datetime.now(tz)
    expire_at = now + (expire_timedelta or timedelta(minutes=expire_minutes))
    token = auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )
    tz = timezone("Europe/Moscow")
    return {
        "token": token,
        "expires_in": expire_at.isoformat(),
        "created_at": datetime.now(tz).isoformat(),
    }


def create_access_token(user: User) -> str:
    jwt_payload = {
        # subject
        "sub": str(user.id),
        # "username": user.username
        "email": user.email,
        "role_id": user.role_id,
        # "logged_in_at"
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


async def create_refresh_token(user: Any, fingerprint: str) -> dict:
    jti = str(uuid4())
    jwt_payload = {
        "sub": str(user.id),
        "jti": jti,
        # "username": user.username,
    }
    refresh_token_data = create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(
            days=settings.auth_jwt.refresh_token_expire_days
        ),
    )
    refresh_token_data["fingerprint"] = fingerprint
    refresh_token_data["user_id"] = str(user.id)
    refresh_token_data["jti"] = jti

    return refresh_token_data


async def authenticate(redis, info: Info, user: User) -> tuple[Response, JSON]:
    access_token = create_access_token(user)
    fingerprint = info.context.get("fingerprint")

    refresh_token_data = await create_refresh_token(user, fingerprint)
    await save_refresh_token_to_redis(redis, refresh_token_data)

    response = info.context["response"]
    response.set_cookie(
        key="refreshToken",
        value=refresh_token_data["token"],
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return response, {"accessToken": access_token}
