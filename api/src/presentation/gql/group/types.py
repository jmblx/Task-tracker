import strawberry

from core.utils import GqlProtocol
from presentation.gql.graphql_utils import add_from_instance
from presentation.gql.task.types import TaskType
from presentation.gql.user.types import UserType


@strawberry.type
@add_from_instance
class GroupType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    tasks: list[TaskType] | None = None
    user: UserType | None = None
