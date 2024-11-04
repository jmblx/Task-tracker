from typing import Any, Set, Tuple
import logging

from domain.entities.user.models import User
from domain.services.user.access_policy import UserAccessPolicyInterface
from domain.services.access_policy_interface import AccessCheck


class SelfAccessCheck(AccessCheck):
    override_checks = "*"  # Перекрывает все остальные проверки

    async def get_required_data(self, fields: dict[str, Any]) -> Tuple[dict[str, Any], dict[str, Any]]:
        # Данные о requester не нужны, так как мы используем объект user
        target_data = {"user": {"id": {}}}
        return {}, target_data

    async def execute(self, user: User, target_data: dict[str, Any]) -> bool:
        return user.id == target_data["user"]["id"]


class OrganizationOverlapCheck(AccessCheck):
    override_checks = set()

    async def get_required_data(self, fields: dict[str, Any]) -> Tuple[dict[str, Any], dict[str, Any]]:
        # Данные для target сохраняем в прежнем виде
        target_data = {"user": {"organizations": {"id": {}}}}
        return {}, target_data  # Для requestera не нужны данные, используем объект user

    async def execute(self, user: User, target_data: dict[str, Any]) -> bool:
        requester_orgs = user.organizations
        target_orgs = target_data.get("user", {}).get("organizations", [])
        requester_org_ids = [org.id for org in requester_orgs]
        target_org_ids = [org.id for org in target_orgs]

        return bool(set(requester_org_ids) & set(target_org_ids))


self_access_check = SelfAccessCheck()
organization_overlap_check = OrganizationOverlapCheck()


class UserAccessPolicy(UserAccessPolicyInterface):
    policy_map = {
        "read": {
            "id": {"checks": {self_access_check, organization_overlap_check}},
            "first_name": {"checks": set()},
            "last_name": {"checks": set()},
            "email": {"checks": set()},
            "is_active": {"checks": set()},
            "is_verified": {"checks": set()},
            "registered_at": {"checks": set()},
            "pathfile": {"checks": set()},
            "role_id": {"checks": {self_access_check}},
            "tg_id": {"checks": {self_access_check}},
            "tg_settings": {"checks": {self_access_check}},
            "is_email_confirmed": {"checks": {self_access_check}},
            "organizations": {"checks": {self_access_check}},
            "role": {"checks": {self_access_check}},
            "tasks": {"checks": {organization_overlap_check}},
        },
        "update": {
            "first_name": {"checks": {self_access_check}},  # Only self can update
            "last_name": {"checks": {self_access_check}},  # Only self can update
            "role_id": {"checks": {self_access_check}},  # Role updates only for self
            "email": {"checks": {self_access_check}},  # Only self can update email
            "tg_id": {"checks": {self_access_check}},  # Only self can update tg_id
            "tg_settings": {"checks": {self_access_check}},  # Only self can update tg_settings
            "github_name": {"checks": {self_access_check}},  # Only self can update github_name
        },
        "delete": {
            "*": {"checks": {self_access_check}},  # При удалении всегда используется SelfAccessCheck
        }
    }

    async def get_required_data(
        self, action: str, fields: dict[str, Any] | None = None
    ) -> Tuple[dict[str, Any], dict[str, Any], Set[AccessCheck]]:
        if fields is None:
            fields = {"*": {}}
        target_data = {"user": {}}
        checks_to_execute = set()

        normalized_fields = self.normalize_fields(fields)

        for field, subfields in normalized_fields.items():
            if field in self.policy_map[action]:
                checks = self.policy_map[action][field]["checks"]
                checks_to_execute.update(checks)

        if any(check.override_checks == "*" for check in checks_to_execute):
            checks_to_execute = {check for check in checks_to_execute if check.override_checks == "*"}

        for check in checks_to_execute:
            _, tgt_data = await check.get_required_data(normalized_fields)
            target_data["user"].update(tgt_data.get("user", {}))

        return {}, target_data, checks_to_execute

    def normalize_fields(self, fields: dict[str, Any]) -> dict[str, dict]:
        """
        Преобразует формат данных для обновления из {'first_name': 'new'} в {'first_name': {}}
        """
        normalized = {}
        for field, value in fields.items():
            if isinstance(value, dict):
                normalized[field] = value
            else:
                normalized[field] = {}
        return normalized

    async def check_access(
        self, user: User, target_data: dict[str, Any], checks: Set[AccessCheck]
    ) -> bool:
        # Выполняем проверки
        for check in checks:
            if not await check.execute(user, target_data):
                return False

        return True
