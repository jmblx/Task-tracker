from dataclasses import dataclass
from uuid import UUID

from application.dtos.base import BaseDTO


@dataclass
class GroupCreateDTO(BaseDTO):
    name: str
    user_id: UUID
