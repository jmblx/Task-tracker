from typing import Any, Set, Tuple

from domain.entities.user.models import User
from domain.services.project.access_policy import ProjectAccessPolicyInterface
from domain.services.access_policy_interface import AccessCheck
from domain.services.user.access_policy import UserAccessPolicyInterface


class RolePermissionCheck(AccessCheck):
    override_checks = set()

    async def get_required_data(
        self, fields: dict[str, Any]
    ) -> Tuple[dict[str, Any], dict[str, Any]]:
        requester_data = {"user": {"role": {"permissions": {"project": {}}}}}
        return requester_data, {}

    async def execute(self, user: User, target_data: dict[str, Any]) -> bool:
        return user.role.permissions.get("project", False)


class OrganizationMembershipCheck(AccessCheck):
    override_checks = set()

    async def get_required_data(
        self, fields: dict[str, Any]
    ) -> Tuple[dict[str, Any], dict[str, Any]]:
        requester_data = {"user": {"organizations": {"id": {}}}}
        target_data = {"project": {"organization_id": {}}}
        return requester_data, target_data

    async def execute(self, user: User, target_data: dict[str, Any]) -> bool:
        user_org_ids = [org.id for org in user.organizations]
        project_org_id = target_data["project"]["organization_id"]
        return project_org_id in user_org_ids


role_permission_check = RolePermissionCheck()
organization_membership_check = OrganizationMembershipCheck()


class ProjectAccessPolicy(ProjectAccessPolicyInterface):
    policy_map = {
        "read": {
            "*": {"checks": set()},  # Общий доступ ко всем полям по умолчанию
            "tasks": {"checks": {organization_membership_check}},  # Ограниченный доступ к задачам
        },
        "create": {
            "*": {"checks": {role_permission_check, organization_membership_check}},
        },
        # Здесь можно добавить другие действия (update, delete)
    }

    async def get_required_data(
        self, action: str, fields: dict[str, Any] | None = None
    ) -> Tuple[dict[str, Any], dict[str, Any], Set[AccessCheck]]:
        if fields is None:
            fields = {"*": {}}
        requester_data = {}
        target_data = {}
        checks_to_execute = set()

        normalized_fields = self.normalize_fields(fields)

        for field, subfields in normalized_fields.items():
            if field in self.policy_map[action]:
                checks = self.policy_map[action][field]["checks"]
                checks_to_execute.update(checks)
            elif "*" in self.policy_map[action]:
                checks = self.policy_map[action]["*"]["checks"]
                checks_to_execute.update(checks)

        # Проверка на override
        if any(check.override_checks == "*" for check in checks_to_execute):
            checks_to_execute = {
                check for check in checks_to_execute if check.override_checks == "*"
            }

        # Сбор необходимых данных
        for check in checks_to_execute:
            req_data_requester, req_data_target = await check.get_required_data(normalized_fields)
            # Объединяем данные
            requester_data = self.merge_data(requester_data, req_data_requester)
            target_data = self.merge_data(target_data, req_data_target)

        return requester_data, target_data, checks_to_execute

    def merge_data(self, data1: dict, data2: dict) -> dict:
        for key, value in data2.items():
            if key in data1 and isinstance(data1[key], dict) and isinstance(value, dict):
                data1[key] = self.merge_data(data1[key], value)
            else:
                data1[key] = value
        return data1

    async def check_access(
        self, user: User, target_data: dict[str, Any], checks: Set[AccessCheck]
    ) -> bool:
        for check in checks:
            if not await check.execute(user, target_data):
                return False
        return True

    def normalize_fields(self, fields: dict[str, Any]) -> dict[str, dict]:
        """
        Преобразует формат данных для чтения из {'tasks': {}} в {'tasks': {}}
        """
        normalized = {}
        for field, value in fields.items():
            if isinstance(value, dict):
                normalized[field] = value
            else:
                normalized[field] = {}
        return normalized
