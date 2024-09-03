import strawberry
from strawberry import Info

from domain.entities.task.models import Task
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.task.inputs import TaskFindType
from presentation.gql.task.types import TaskType


@strawberry.type
class TaskQuery:
    @strawberry.field
    @strawberry_read(Task, TaskType, "getTask", need_validation=True)
    async def get_task(
        self,
        info: Info,
        search_data: TaskFindType,
        order_by: OrderByInput | None = None,
    ) -> list[TaskType] | None:
        pass
