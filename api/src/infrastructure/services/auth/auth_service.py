import logging
from datetime import timedelta, datetime
from typing import Dict, Any
from uuid import uuid4

from fastapi import HTTPException
from jwt import DecodeError, ExpiredSignatureError
from pytz import timezone
from redis.asyncio import Redis

from config import JWTSettings
from domain.entities.user.models import User
from domain.services.auth.auth_service import AuthService
from domain.services.auth.jwt_service import JWTService
from domain.services.security.pwd_service import HashService
from domain.services.user.service import UserServiceInterface
from infrastructure.services.user.service_impl import UserServiceImpl
from infrastructure.external_services.myredis.utils import (
    save_refresh_token_to_redis,
)

logger = logging.getLogger(__name__)


class AuthServiceImpl(AuthService):
    def __init__(
        self,
        jwt_service: JWTService,
        user_service: UserServiceInterface,
        redis: Redis,
        auth_settings: JWTSettings,
        hash_service: HashService,
    ):
        self.jwt_service = jwt_service
        self.user_service = user_service
        self.redis = redis
        self.auth_settings = auth_settings
        self.hash_service = hash_service

    async def authenticate_and_return_user(
        self, email: str, password: str
    ) -> User:
        user = await self.user_service.get_by_fields(
            {"email": email},
            {"id": {}, "hashed_password": {}, "email": {}, "role_id": {}},
        )
        if not user or not self.hash_service.check_password(
            password, user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    async def refresh_access_token(
        self, refresh_token: str, fingerprint: str
    ) -> str:
        payload = self.jwt_service.decode(refresh_token)
        jti = payload.get("jti")
        token_data = await self.redis.hgetall(f"refresh_token:{jti}")

        if not token_data or token_data.get("fingerprint") != fingerprint:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token or fingerprint"
            )

        user = await self.user_service.get_by_id(payload.get("sub"))
        return self.create_access_token(user)

    async def create_tokens(
        self, user: User, fingerprint: str
    ) -> tuple[str, str]:
        access_token = self.create_access_token(user)
        refresh_token_data = await self.create_refresh_token(user, fingerprint)
        print(refresh_token_data)
        await self.save_refresh_token_to_redis(
            refresh_token_data, self.auth_settings
        )
        return access_token, refresh_token_data["token"]

    async def validate_permission(
        self, token: str, entity: str, permission: str
    ) -> bool:
        try:
            user = await self.get_user_by_token(token)
        except (ExpiredSignatureError, DecodeError):
            raise HTTPException(status_code=401, detail="Invalid token")

        entity_permissions = user.role.permissions.get(entity)
        if permission not in entity_permissions:
            raise HTTPException(status_code=403, detail="Permission denied")

        return True

    def create_access_token(self, user: User) -> str:
        jwt_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role_id": user.role_id,
        }
        return self.jwt_service.encode(
            payload=jwt_payload,
            expire_minutes=self.auth_settings.access_token_expire_minutes,
        )

    async def create_refresh_token(self, user: User, fingerprint: str) -> dict:
        jti = str(uuid4())
        jwt_payload = {"sub": str(user.id), "jti": jti}
        refresh_token_data = self.jwt_service.encode(
            payload=jwt_payload,
            expire_timedelta=timedelta(
                days=self.auth_settings.refresh_token_expire_days
            ),
        )
        refresh_token_data.update(
            {"user_id": str(user.id), "jti": jti, "fingerprint": fingerprint}
        )
        return refresh_token_data

    async def get_user_by_token(self, token: str) -> User:
        """Получает пользователя по токену."""
        payload = self.jwt_service.decode(token)
        user_id = payload.get("sub")
        return await self.user_service.get_by_id(user_id)

    async def get_refresh_token_data(
        self, refresh_token: str
    ) -> Dict[str, Any]:
        payload = self.jwt_service.decode(refresh_token)
        jti = payload.get("jti")
        token_data = await self.redis.hgetall(f"refresh_token:{jti}")
        return token_data

    async def save_refresh_token_to_redis(
        self,
        refresh_token_data: dict,
        auth_settings: "JWTSettings",
    ) -> None:
        jti = str(refresh_token_data.pop("jti"))
        user_id = refresh_token_data["user_id"]
        fingerprint = refresh_token_data["fingerprint"]
        created_at = datetime.fromisoformat(
            refresh_token_data["created_at"]
        ).timestamp()

        existing_jti = await self.redis.get(
            f"refresh_token_index:{user_id}:{fingerprint}"
        )
        if existing_jti:
            logging.info("Found existing token with jti: %s", existing_jti)
            await self.redis.delete(f"refresh_token:{existing_jti}")
            await self.redis.zrem(f"refresh_tokens:{user_id}", existing_jti)
        else:
            logging.info(
                "No existing token found for user_id: %s and fingerprint: %s",
                user_id,
                fingerprint,
            )

        await self.redis.hset(
            f"refresh_token:{jti}", mapping=refresh_token_data
        )
        await self.redis.set(
            f"refresh_token_index:{user_id}:{fingerprint}", jti
        )
        logging.info("Saved new token with jti: %s", jti)

        await self.redis.zadd(f"refresh_tokens:{user_id}", {jti: created_at})

        num_tokens = await self.redis.zcard(f"refresh_tokens:{user_id}")
        if num_tokens > auth_settings.refresh_token_by_user_limit:
            oldest_jti_list = await self.redis.zrange(
                f"refresh_tokens:{user_id}", 0, 0
            )
            if oldest_jti_list:
                oldest_jti = oldest_jti_list[0]
                logging.info("Removing oldest token with jti: %s", oldest_jti)
                await self.redis.zrem(f"refresh_tokens:{user_id}", oldest_jti)
                await self.redis.delete(f"refresh_token:{oldest_jti}")
        else:
            logging.info(
                "Number of tokens for user_id %s is within limit: %s",
                user_id,
                num_tokens,
            )
