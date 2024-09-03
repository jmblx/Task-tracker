from uuid import UUID

import strawberry
from strawberry.scalars import JSON

from presentation.gql.scalars import DateTime, Duration


@strawberry.input
class TaskFindType:
    id: int | None = None
    name: str | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None


@strawberry.input
class AssigneeType:
    id: UUID | None = None
    github_data: JSON | None = None
    organization_id: int | None = None


@strawberry.input
class TaskCreateType:
    name: str
    description: str | None = None
    is_done: bool | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    duration: Duration
    end_date: DateTime | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None
    assignees: list[AssigneeType] | None = None


@strawberry.input
class TaskUpdateType:
    name: str | None = None
    description: str | None = None
    is_done: bool | None = None
    assigner_id: UUID | None = None
    color: str | None = None
    duration: Duration | None = None
    end_date: DateTime | None = None
    difficulty: str | None = None
    project_id: int | None = None
    group_id: int | None = None
