import strawberry
from strawberry import Info

from application.usecases.project.read import ReadProjectUseCase
from core.di.container import container
from core.db.utils import get_selected_fields
from presentation.gql.gql_types import OrderByInput
from presentation.gql.project.inputs import ProjectFindType
from presentation.gql.project.types import ProjectType


@strawberry.type
class ProjectQuery:
    @strawberry.field
    async def get_project(
        self,
        info: Info,
        search_data: ProjectFindType,
        order_by: OrderByInput | None = None,
    ) -> list[ProjectType] | None:
        auth_token = info.context.get("auth_token")
        async with container() as ioc:
            interactor = await ioc.get(ReadProjectUseCase)
            selected_fields = get_selected_fields(info, "getProject")
            projects = await interactor(
                auth_token, search_data.__dict__, selected_fields, order_by
            )
            return [ProjectType.from_instance(project, selected_fields) for project in projects]
