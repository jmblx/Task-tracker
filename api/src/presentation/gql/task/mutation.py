import strawberry
from strawberry import Info

from application.usecases.task.create import CreateTaskAndReadUseCase
from application.usecases.task.delete import (
    DeleteAndReadTaskUseCase,
    DeleteTaskUseCase,
)
from application.usecases.task.update import (
    UpdateTaskAndReadUseCase,
)
from core.db.utils import get_selected_fields
from core.di.container import container
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import decrease_task_time_by_id
from presentation.gql.task.inputs import (
    TaskCreateType,
    TaskFindType,
    TaskUpdateType,
)
from presentation.gql.task.types import TaskType


@strawberry.type
class TaskMutation:
    @strawberry.mutation
    async def add_task(self, info: Info, data: TaskCreateType) -> TaskType:
        async with container() as ioc:
            interactor = await ioc.get(CreateTaskAndReadUseCase)
            selected_fields = get_selected_fields(info, "addTask")
            task = await interactor(data.__dict__, selected_fields)
            return TaskType.from_instance(task, selected_fields)

    @strawberry.mutation
    async def update_tasks_with_response(
        self,
        info: Info,
        search_data: TaskFindType,
        data: TaskUpdateType,
        order_by: OrderByInput | None = None,
    ) -> list[TaskType]:
        async with container() as ioc:
            upd_data = {key: value for key, value in data.__dict__.items() if value is not None}
            interactor = await ioc.get(UpdateTaskAndReadUseCase)
            selected_fields = get_selected_fields(info, "updateTasksWithResponse")
            tasks = await interactor(
                search_data.__dict__, upd_data, selected_fields,
                order_by.__dict__ if order_by is not None else None,
            )
            return [TaskType.from_instance(task, selected_fields) for task in tasks]

    @strawberry.mutation
    async def delete_task(
        self,
        search_data: TaskFindType,
        full_delete: bool = False
    ) -> bool:
        async with container() as ioc:
            interactor = await ioc.get(DeleteTaskUseCase)
            await interactor(search_data.__dict__, full_delete)
            return True

    @strawberry.mutation
    async def delete_tasks_with_response(
        self,
        info: Info,
        search_data: TaskFindType,
        order_by: OrderByInput | None = None,
        full_delete: bool = False,
    ) -> list[TaskType]:
        async with container() as ioc:
            interactor = await ioc.get(DeleteAndReadTaskUseCase)
            selected_fields = get_selected_fields(info, "deleteTasksWithResponse")
            tasks = await interactor(
                search_data.__dict__, selected_fields,
                order_by.__dict__ if order_by is not None else None, full_delete
            )
            return [TaskType.from_instance(task, selected_fields) for task in tasks]

    @strawberry.mutation
    async def decrease_task_time(self, item_id: int, seconds: int) -> bool:
        await decrease_task_time_by_id(item_id, seconds)
        return True
