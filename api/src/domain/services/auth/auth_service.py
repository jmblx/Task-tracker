from abc import ABC, abstractmethod
from typing import Any

from redis.asyncio import Redis

from config import JWTSettings


class AuthService(ABC):
    @abstractmethod
    async def authenticate_and_return_user(
        self, email: str, password: str
    ) -> Any:
        """Аутентифицирует пользователя по email и паролю."""

    @abstractmethod
    async def refresh_access_token(
        self, refresh_token: str, fingerprint: str
    ) -> str:
        """Обновляет access токен по refresh токену."""

    @abstractmethod
    async def create_tokens(
        self, user: Any, fingerprint: str
    ) -> tuple[str, str]:
        """Создает access и refresh токены для пользователя."""

    @abstractmethod
    async def validate_permission(
        self, token: str, entity: str, permission: str
    ) -> bool:
        """Проверяет, имеет ли пользователь право на выполнение определенного действия."""

    @abstractmethod
    async def save_refresh_token_to_redis(
        self,
        refresh_token_data: dict,
        auth_settings: JWTSettings,
    ) -> None: ...
