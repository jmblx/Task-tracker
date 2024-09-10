from datetime import datetime, timedelta
from typing import Any

import jwt
from pytz import timezone

from config import JWTSettings
from domain.services.auth.jwt_service import JWTService


class JWTServiceImpl(JWTService):
    def __init__(self, auth_settings: JWTSettings):
        self.auth_settings = auth_settings

    def encode(
        self,
        payload: dict,
        expire_minutes: int = None,
        expire_timedelta: timedelta = None,
    ) -> dict[str, Any]:
        tz = timezone("Europe/Moscow")
        now = datetime.now(tz)

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(
                minutes=expire_minutes
                or self.auth_settings.access_token_expire_minutes
            )

        payload.update(
            exp=expire,
            iat=now,
        )
        token = jwt.encode(
            payload,
            self.auth_settings.private_key,
            algorithm=self.auth_settings.algorithm,
        )
        return {
            "token": token,
            "expires_in": expire.isoformat(),
            "created_at": now.isoformat(),
        }

    def decode(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.auth_settings.public_key,
            algorithms=[self.auth_settings.algorithm],
        )
