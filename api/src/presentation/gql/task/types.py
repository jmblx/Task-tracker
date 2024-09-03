from typing import TYPE_CHECKING, Annotated
from uuid import UUID

import strawberry

from core.utils import GqlProtocol
from presentation.gql.graphql_utils import add_from_instance
from presentation.gql.scalars import DateTime, Duration

if TYPE_CHECKING:
    from presentation.gql.user.types import UserType


@strawberry.type
@add_from_instance
class TaskType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    is_done: bool | None = None
    added_at: DateTime | None = None
    done_at: DateTime | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    duration: Duration | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None
    assignees: (
        list[
            Annotated[
                "UserType", strawberry.lazy("presentation.gql.user.types")
            ]
        ]
        | None
    ) = None
    assigner: (
        Annotated["UserType", strawberry.lazy("presentation.gql.user.types")]
        | None
    ) = None
