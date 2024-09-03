import strawberry
from strawberry import Info

from domain.entities.project.models import Project
from presentation.gql.gql_types import OrderByInput
from presentation.gql.graphql_utils import strawberry_read
from presentation.gql.project.inputs import ProjectFindType
from presentation.gql.project.types import ProjectType


@strawberry.type
class ProjectQuery:
    @strawberry.field
    @strawberry_read(Project, ProjectType, "getProject", need_validation=True)
    async def get_project(
        self,
        info: Info,
        search_data: ProjectFindType,
        order_by: OrderByInput | None = None,
    ) -> list[ProjectType] | None:
        pass
