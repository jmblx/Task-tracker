from typing import TYPE_CHECKING, Annotated

import strawberry

from core.utils import GqlProtocol
from presentation.gql.graphql_utils import add_from_instance
from presentation.gql.scalars import DateTime

if TYPE_CHECKING:
    from presentation.gql.task.types import TaskType


@strawberry.type
@add_from_instance
class ProjectType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    created_at: DateTime | None = None
    organization_id: int | None = None
    tasks: (
        list[
            Annotated[
                "TaskType", strawberry.lazy("presentation.gql.task.types")
            ]
        ]
        | None
    ) = None
