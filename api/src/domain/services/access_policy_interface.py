from abc import abstractmethod, ABC
from typing import Dict, Any

from domain.entities.user.models import User


class AccessCheck(ABC):
    @abstractmethod
    async def get_required_data(self, fields: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        pass

    @abstractmethod
    async def execute(self, user: User, target_data: dict[str, Any]) -> bool:
        pass


class BaseAccessPolicyInterface(ABC):
    @abstractmethod
    async def get_required_data(self, action: str, fields=None) -> Dict[str, Any]:
        """
        Метод для получения необходимых данных на основе действия и полей.

        :param action: Действие, которое пытается выполнить пользователь (например, "read").
        :param fields: Поля, к которым пытается получить доступ пользователь.
        :return: Словарь с требуемыми данными для проверки доступа.
        """
        pass

    @abstractmethod
    async def check_access(
        self, user: User, target_data: dict[str, Any], checks: set[AccessCheck]
    ):
        """
        Метод для проверки, имеет ли пользователь доступ к указанным полям на основе действия.

        :param user: Объект пользователя, который выполняет запрос.
        :param action: Действие, которое пытается выполнить пользователь.
        :param fields: Поля, к которым пользователь запрашивает доступ.
        :param data: Необходимые данные для проверки.
        :return: True, если доступ разрешен, иначе False.
        """
        pass
