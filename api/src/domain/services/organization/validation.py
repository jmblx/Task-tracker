from abc import ABC, abstractmethod


class OrganizationValidationService(ABC):
    @abstractmethod
    def validate_create_data(self, organization: dict):
        pass
