from abc import ABC, abstractmethod


class ProjectValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, project: dict):
        pass
