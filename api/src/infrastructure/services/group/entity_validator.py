from core.exceptions.groups.valdiation import InvalidGroupData


class CreateGroupValidator:
    def validate_create_data(self, group: dict) -> None:
        self._validate_bound(group)

    @staticmethod
    def _validate_bound(group: dict):
        if group.get("user_id") is None and group.get("project_id") is None:
            raise InvalidGroupData("user_id or project_id is required")
