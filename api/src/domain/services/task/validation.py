from abc import ABC, abstractmethod


class TaskValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, task: dict):
        pass
