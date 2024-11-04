import strawberry
from strawberry import Info

from application.usecases.task.read import ReadTaskUseCase
from core.db.utils import get_selected_fields
from core.di.container import container
from presentation.gql.gql_types import OrderByInput
from presentation.gql.task.inputs import TaskFindType
from presentation.gql.task.types import TaskType


@strawberry.type
class TaskQuery:
    @strawberry.field
    async def get_task(
        self,
        info: Info,
        search_data: TaskFindType,
        order_by: OrderByInput | None = None,
    ) -> list[TaskType] | None:
        async with container() as ioc:
            interactor = await ioc.get(ReadTaskUseCase)
            selected_fields = get_selected_fields(info, "getTask")
            tasks = await interactor(
                search_data.__dict__, selected_fields, order_by
            )
            return [TaskType.from_instance(task, selected_fields) for task in tasks]

