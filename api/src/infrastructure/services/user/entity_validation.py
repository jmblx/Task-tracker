import re

from core.exceptions.auth.validation import InvalidRegData
from domain.services.user.validation import UserValidationService


class RegUserValidationService(UserValidationService):
    def validate_create_data(self, user_data: dict):
        """
        Выполняет все необходимые проверки для валидации данных пользователя.
        """
        self._validate_email(user_data.get("email"))
        self._validate_password(user_data.get("password"))
        self._validate_name(
            user_data.get("first_name"), user_data.get("last_name")
        )

    @staticmethod
    def _validate_password(password: str):
        """Проверяет, что пароль состоит минимум из 8-и символов,
        содержит хотя бы одну цифру и не содержит пробелов."""
        if not re.match(r"^(?=.*\d)\S{8,}$", password):
            raise InvalidRegData(
                "Invalid password. Password must be at least 8 characters"
                " long and contain at least one digit and one letter."
            )

    @staticmethod
    def _validate_email(email: str):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_regex, email) and len(email) < 255:
            raise InvalidRegData("Invalid email")

    @staticmethod
    def _validate_name(first_name: str, last_name: str):
        name_regex = r"^[a-zA-Zа-яА-ЯёЁ' -]{1,49}$"

        if not re.match(name_regex, first_name) and re.match(
            name_regex, last_name
        ):
            raise InvalidRegData(
                "Name must be between 1 and 49 characters."
                " And contain only letters and ', -, space"
            )
