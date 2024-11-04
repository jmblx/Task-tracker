from abc import ABC, abstractmethod


class HashService(ABC):

    @abstractmethod
    def hash_password(self, password: str) -> bytes:
        pass

    @abstractmethod
    def check_password(
        self, plain_password: str, hashed_password: bytes
    ) -> bool:
        pass
