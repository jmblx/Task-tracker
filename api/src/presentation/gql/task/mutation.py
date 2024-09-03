import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from domain.entities.task.models import Task
from presentation.gql.graphql_utils import (
    decrease_task_time_by_id,
    process_task_assignees,
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
    task_preprocess,
)
from presentation.gql.task.inputs import TaskCreateType, TaskUpdateType
from presentation.gql.task.types import TaskType


@strawberry.type
class TaskMutation:
    @strawberry.mutation
    @strawberry_insert(
        Task,
        data_process_extra=task_preprocess,
        process_extra_db=process_task_assignees,
        exc_fields=["assignees"],
    )
    async def add_task(self, info: Info, data: TaskCreateType) -> TaskType:
        pass

    @strawberry.mutation
    @strawberry_update(Task)
    async def update_task(
        self, info: Info, item_id: int, data: TaskUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Task)
    async def update_task_with_response(
        self, info: Info, item_id: int, data: TaskUpdateType
    ) -> TaskType:
        pass

    @strawberry.mutation
    @strawberry_delete(Task)
    async def delete_task(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Task)
    async def delete_task_with_response(
        self, info: Info, item_id: int
    ) -> TaskType:
        pass

    @strawberry.mutation
    async def decrease_task_time(self, item_id: int, seconds: int) -> bool:
        await decrease_task_time_by_id(item_id, seconds)
        return True
