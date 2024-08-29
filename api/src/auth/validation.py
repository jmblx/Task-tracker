from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from strawberry import Info

from auth import jwt_utils
from auth.crud import get_user_by_email
from auth.helpers import (
    ACCESS_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)
from auth.models import User
from db.utils import get_user_by_id, get_user_by_token

if TYPE_CHECKING:
    from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = jwt_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r}"
        f" expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> User:
    user_id: UUID | None = payload.get("sub")
    if user := await get_user_by_id(user_id, session):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> User:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        session: AsyncSession,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload, session)


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

# get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


async def validate_auth_user(
    email: str,
    password: str,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := await get_user_by_email(email)):
        raise unauthed_exc

    if not jwt_utils.validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


async def validate_permission(info: Info, entity: str, permission: str):
    try:
        token = info.context.get("auth_token").replace("Bearer ", "")
        user = await get_user_by_token(token)
    except (ExpiredSignatureError, DecodeError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)  # noqa: B904
    entity_permissions = user.role.permissions.get(entity)
    if permission not in entity_permissions:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)
