import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from domain.entities.project.models import Project
from presentation.gql.graphql_utils import (
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
)
from presentation.gql.project.inputs import (
    ProjectCreateType,
    ProjectUpdateType,
)
from presentation.gql.project.types import ProjectType


@strawberry.type
class ProjectMutation:
    @strawberry.mutation
    @strawberry_insert(Project)
    async def add_project(
        self, info: Info, data: ProjectCreateType
    ) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_update(Project)
    async def update_project(
        self, info: Info, item_id: int, data: ProjectUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Project)
    async def update_project_with_response(
        self, info: Info, item_id: int, data: ProjectUpdateType
    ) -> ProjectType:
        pass

    @strawberry.mutation
    @strawberry_delete(Project)
    async def delete_project(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Project)
    async def delete_project_with_response(
        self, info: Info, item_id: int
    ) -> ProjectType:
        pass
