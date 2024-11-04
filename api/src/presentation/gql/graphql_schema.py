import strawberry
from fastapi import UploadFile
from strawberry.extensions import QueryDepthLimiter
from strawberry.file_uploads import Upload

from presentation.gql.auth.mutation import AuthMutation
from presentation.gql.auth.query import AuthQuery
from presentation.gql.group.mutation import GroupMutation
from presentation.gql.group.query import GroupQuery
from presentation.gql.organization.mutation import OrganizationMutation
from presentation.gql.organization.query import OrganizationQuery
from presentation.gql.project.mutation import ProjectMutation
from presentation.gql.project.query import ProjectQuery
from presentation.gql.role.mutation import RoleMutation
from presentation.gql.role.query import RoleQuery
from presentation.gql.scalars import DateTime, Duration
from presentation.gql.task.mutation import TaskMutation
from presentation.gql.task.query import TaskQuery
from presentation.gql.user.mutation import UserMutation
from presentation.gql.user.query import UserQuery


@strawberry.type
class Query(
    AuthQuery,
    GroupQuery,
    OrganizationQuery,
    ProjectQuery,
    RoleQuery,
    TaskQuery,
    UserQuery,
):
    pass


@strawberry.type
class Mutation(
    AuthMutation,
    GroupMutation,
    OrganizationMutation,
    ProjectMutation,
    RoleMutation,
    TaskMutation,
    UserMutation,
):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    types=[DateTime, Duration],
    extensions=[
        QueryDepthLimiter(max_depth=3),
        # SQLAlchemySession
    ],
    scalar_overrides={UploadFile: Upload},
)
