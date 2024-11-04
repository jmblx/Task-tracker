from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError
from pytz import timezone

from config import JWTSettings


def encode_jwt(
    payload: dict,
    auth_settings: Optional["JWTSettings"] = None,
    expire_minutes: int | None = None,
    expire_timedelta: timedelta | None = None,
) -> str:
    expire_minutes = (
        expire_minutes
        if expire_minutes
        else auth_settings.access_token_expire_minutes
    )
    to_encode = payload.copy()
    tz = timezone("Europe/Moscow")
    now = datetime.now(tz)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes or expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    return jwt.encode(
        to_encode, auth_settings.private_key, algorithm=auth_settings.algorithm
    )


def decode_jwt(token: str | bytes, auth_settings: JWTSettings) -> dict:
    return jwt.decode(
        token,
        auth_settings.public_key,
        algorithms=[auth_settings.algorithm],
    )


# def hash_password(
#     password: str,
# ) -> bytes:
#     salt = bcrypt.gensalt()
#     pwd_bytes: bytes = password.encode()
#     return bcrypt.hashpw(pwd_bytes, salt)
#
#
# def validate_password(
#     password: str,
#     hashed_password: bytes,
# ) -> bool:
#     return bcrypt.checkpw(
#         password=password.encode(),
#         hashed_password=hashed_password,
#     )


ph = PasswordHasher()


def hash_password(password: str) -> bytes:
    hashed_password_str = ph.hash(password)
    return hashed_password_str.encode("utf-8")


def validate_password(password: str, hashed_password: bytes) -> bool:
    try:
        hashed_password_str = hashed_password.decode("utf-8")
        ph.verify(hashed_password_str, password)
        return True
    except VerifyMismatchError:
        return False
    except InvalidHash:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
