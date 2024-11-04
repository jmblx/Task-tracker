# from core.exceptions.roles.valdiation import InvalidProjectData


class CreateProjectValidator:
    def validate_create_data(self, project: dict) -> None:
        self._validate_bound(project)
