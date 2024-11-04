from abc import ABC, abstractmethod


class GroupValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, group: dict):
        pass
