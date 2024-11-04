from abc import ABC, abstractmethod


class RoleValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, role: dict):
        pass
