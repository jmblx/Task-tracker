from abc import ABC

from domain.services.access_policy_interface import BaseAccessPolicyInterface


class UserAccessPolicyInterface(BaseAccessPolicyInterface, ABC): ...
