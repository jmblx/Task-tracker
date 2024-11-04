import strawberry
from strawberry import Info

from application.usecases.project.create import CreateProjectAndReadUseCase
from application.usecases.project.delete import (
    DeleteAndReadProjectUseCase,
    DeleteProjectUseCase,
)
from application.usecases.project.update import (
    UpdateProjectUseCase, UpdateProjectAndReadUseCase,
)
from core.db.utils import get_selected_fields
from core.di.container import container
from presentation.gql.gql_types import OrderByInput
from presentation.gql.project.inputs import (
    ProjectCreateType,
    ProjectFindType,
    ProjectUpdateType,
)
from presentation.gql.project.types import ProjectType


@strawberry.type
class ProjectMutation:
    @strawberry.mutation
    async def add_project(self, info: Info, data: ProjectCreateType) -> ProjectType:
        auth_token = info.context.get("auth_token")
        async with container() as ioc:
            interactor = await ioc.get(CreateProjectAndReadUseCase)
            selected_fields = get_selected_fields(info, "addProject")
            project = await interactor(auth_token, data.__dict__, selected_fields)
            return ProjectType.from_instance(project, selected_fields)

    @strawberry.mutation
    async def update_projects_with_response(
        self,
        info: Info,
        search_data: ProjectFindType,
        data: ProjectUpdateType,
        order_by: OrderByInput | None = None,
    ) -> list[ProjectType]:
        async with container() as ioc:
            upd_data = {key: value for key, value in data.__dict__.items() if value is not None}
            interactor = await ioc.get(UpdateProjectAndReadUseCase)
            selected_fields = get_selected_fields(info, "updateProjectsWithResponse")
            projects = await interactor(
                search_data.__dict__, upd_data, selected_fields,
                order_by.__dict__ if order_by is not None else None,
            )
            return [ProjectType.from_instance(project, selected_fields) for project in projects]

    @strawberry.mutation
    async def update_projects(
        self,
        search_data: ProjectFindType,
        data: ProjectUpdateType,
    ) -> bool:
        async with container() as ioc:
            upd_data = {key: value for key, value in data.__dict__.items() if value is not None}
            interactor = await ioc.get(UpdateProjectUseCase)
            await interactor(search_data.__dict__, upd_data)
            return True

    @strawberry.mutation
    async def delete_project(
        self,
        search_data: ProjectFindType,
        full_delete: bool = False
    ) -> bool:
        async with container() as ioc:
            interactor = await ioc.get(DeleteProjectUseCase)
            await interactor(search_data.__dict__, full_delete)
            return True

    @strawberry.mutation
    async def delete_projects_with_response(
        self,
        info: Info,
        search_data: ProjectFindType,
        order_by: OrderByInput | None = None,
        full_delete: bool = False,
    ) -> list[ProjectType]:
        async with container() as ioc:
            interactor = await ioc.get(DeleteAndReadProjectUseCase)
            selected_fields = get_selected_fields(info, "deleteProjectsWithResponse")
            projects = await interactor(
                search_data.__dict__, selected_fields,
                order_by.__dict__ if order_by is not None else None, full_delete
            )
            return [ProjectType.from_instance(project, selected_fields) for project in projects]
