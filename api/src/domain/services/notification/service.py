from abc import ABC, abstractmethod


class NotifyService(ABC):
    @abstractmethod
    async def email_register_notify(self, data: dict) -> None:
        pass

    @abstractmethod
    async def pwd_reset_notify(self, user_email: str) -> str:
        pass
