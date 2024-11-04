from abc import ABC, abstractmethod


class UserValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, user_data: dict): ...
