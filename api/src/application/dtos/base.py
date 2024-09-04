from abc import ABC
from uuid import UUID


class BaseDTO(ABC):
    """
    Базовый класс для всех DTO в проекте.
    Можно определить общие методы или атрибуты, если необходимо.
    """

    id: UUID | int
