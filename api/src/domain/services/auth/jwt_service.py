from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any


class JWTService(ABC):
    @abstractmethod
    def encode(
        self,
        payload: dict,
        expire_minutes: int = None,
        expire_timedelta: timedelta = None,
    ) -> dict[str, Any]:
        """Кодирует данные в JWT токен."""

    @abstractmethod
    def decode(self, token: str) -> dict:
        """Декодирует JWT токен в словарь данных."""
