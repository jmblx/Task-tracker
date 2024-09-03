from abc import abstractmethod, ABC


class NotifyService(ABC):
    @abstractmethod
    async def email_register_notify(self, data: dict) -> None:
        pass
