from abc import ABC, abstractmethod

from application.dtos.user import UserCreateDTO


class UserValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, user_data: dict): ...
