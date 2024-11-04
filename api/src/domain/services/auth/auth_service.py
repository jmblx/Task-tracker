from abc import ABC, abstractmethod
from typing import Any

from config import JWTSettings
from domain.entities.user.models import User


class AuthService(ABC):
    @abstractmethod
    async def authenticate_and_return_user(
        self, email: str, password: str
    ) -> User:
        """Аутентифицировать пользователя и вернуть объект пользователя."""

    @abstractmethod
    async def refresh_access_token(
        self, refresh_token: str, fingerprint: str
    ) -> str:
        """Обновить токен доступа по токену обновления и отпечатку."""

    @abstractmethod
    async def create_tokens(
        self, user: User, fingerprint: str
    ) -> tuple[str, str]:
        """Создать токены доступа и обновления для пользователя."""

    @abstractmethod
    async def validate_permission(
        self, token: str, entity: str, permission: str
    ) -> bool:
        """Проверить разрешения пользователя на выполнение определенного действия."""

    @abstractmethod
    def create_access_token(self, user: User) -> str:
        """Создать токен доступа для пользователя."""

    @abstractmethod
    async def create_refresh_token(self, user: User, fingerprint: str) -> dict:
        """Создать токен обновления для пользователя."""

    @abstractmethod
    async def get_user_by_token(self, token: str, selected_fields: dict) -> User:
        """Получить пользователя по токену."""

    @abstractmethod
    async def get_refresh_token_data(
        self, refresh_token: str
    ) -> dict[str, Any]:
        """Получить данные о токене обновления."""

    @abstractmethod
    async def save_refresh_token_to_redis(
        self, refresh_token_data: dict, auth_settings: "JWTSettings"
    ) -> None:
        """Сохранить токен обновления в Redis."""
