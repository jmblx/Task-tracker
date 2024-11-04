from abc import ABC, abstractmethod
from uuid import UUID


class ResetPwdService(ABC):
    @abstractmethod
    async def save_password_reset_token(
        self, user_id: UUID, token: str
    ) -> None: ...
