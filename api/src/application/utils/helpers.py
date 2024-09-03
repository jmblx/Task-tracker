import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from fastapi import HTTPException
from pytz import timezone
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST
from strawberry import Info
from strawberry.scalars import JSON

from application.utils import jwt_utils as auth_utils
from domain.entities.user.models import User
from infrastructure.external_services.myredis.utils import (
    save_refresh_token_to_redis,
)

if TYPE_CHECKING:
    from config import AuthJWT


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


logger = logging.getLogger(__name__)


def create_jwt(
    token_type: str,
    token_data: dict,
    auth_settings: "AuthJWT",
    expire_minutes: int | None = None,
    expire_timedelta: timedelta | None = None,
) -> dict:
    expire_minutes = (
        expire_minutes or auth_settings.access_token_expire_minutes
    )
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)

    tz = timezone("Europe/Moscow")
    now = datetime.now(tz)
    expire_at = now + (expire_timedelta or timedelta(minutes=expire_minutes))

    token = auth_utils.encode_jwt(
        payload=jwt_payload,
        auth_settings=auth_settings,
        expire_timedelta=expire_timedelta,
    )

    result = {
        "token": token,
        "expires_in": expire_at.isoformat(),
        "created_at": datetime.now(tz).isoformat(),
    }

    return result


def create_access_token(user: User, auth_settings: "AuthJWT") -> str:
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
        auth_settings=auth_settings,
        expire_minutes=auth_settings.access_token_expire_minutes,
    )


async def create_refresh_token(
    user: Any, fingerprint: str, auth_settings: "AuthJWT"
) -> dict:
    jti = str(uuid4())
    jwt_payload = {
        "sub": str(user.id),
        "jti": jti,
        # "username": user.username,
    }
    refresh_token_data = create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        auth_settings=auth_settings,
        expire_timedelta=timedelta(
            days=auth_settings.refresh_token_expire_days
        ),
    )
    refresh_token_data["fingerprint"] = fingerprint
    refresh_token_data["user_id"] = str(user.id)
    refresh_token_data["jti"] = jti

    return refresh_token_data


async def authenticate(
    redis, info: Info, user: User, auth_settings: "AuthJWT"
) -> tuple[Response, JSON]:
    access_token = create_access_token(user, auth_settings)
    fingerprint = info.context.get("fingerprint", None)
    if not fingerprint:
        raise HTTPException(
            HTTP_400_BAD_REQUEST, detail="Fingerprint is required"
        )

    refresh_token_data = await create_refresh_token(
        user, fingerprint, auth_settings
    )
    await save_refresh_token_to_redis(redis, refresh_token_data, auth_settings)

    response = info.context["response"]
    response.set_cookie(
        key="refreshToken",
        value=refresh_token_data["token"],
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return response, {"accessToken": access_token}
