from uuid import UUID

from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from auth.crud import get_user_by_email
from db.utils import get_user_by_id
from auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from auth import jwt_utils
from auth.models import User
from auth.schemas import UserAuth

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
        raise HTTPException(
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
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict) -> User:
    user_id: UUID | None = payload.get("sub")
    if user := await get_user_by_id(user_id):
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
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


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
