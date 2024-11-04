# from core.exceptions.roles.valdiation import InvalidOrganizationData


class CreateOrganizationValidator:
    def validate_create_data(self, organization: dict) -> None:
        self._validate_bound(organization)
