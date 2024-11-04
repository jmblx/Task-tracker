# from core.exceptions.roles.valdiation import InvalidRoleData


class CreateRoleValidator:
    def validate_create_data(self, role: dict) -> None:
        self._validate_bound(role)
