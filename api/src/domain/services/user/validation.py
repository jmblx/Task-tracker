from abc import ABC, abstractmethod


class ValidationService(ABC):
    @abstractmethod
    def validate(self): ...
