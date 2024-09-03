from uuid import UUID

import strawberry

from core.utils import GqlProtocol
from presentation.gql.graphql_utils import add_from_instance
from presentation.gql.organization.query import OrganizationType
from presentation.gql.role.types import RoleType
from presentation.gql.scalars import DateTime
from presentation.gql.task.types import TaskType


@strawberry.type
@add_from_instance
class UserType(GqlProtocol):
    id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    email: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    pathfile: str | None = None
    tg_id: str | None = None
    tg_settings: strawberry.scalars.JSON | None = None
    is_email_confirmed: bool | None = None
    registered_at: DateTime | None = None
    organizations: list["OrganizationType"] | None = None
    role: RoleType | None = None
    tasks: list["TaskType"] | None = None  # Using string annotation here
