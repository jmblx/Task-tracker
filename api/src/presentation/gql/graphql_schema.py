import strawberry
from strawberry.extensions import QueryDepthLimiter

from presentation.gql.auth.query import AuthQuery
from presentation.gql.scalars import DateTime, Duration
from presentation.gql.user.mutation import UserMutation
from presentation.gql.user.query import UserQuery


@strawberry.type
class Query(
    AuthQuery,
    # GroupQuery,
    # OrganizationQuery,
    # ProjectQuery,
    # RoleQuery,
    # TaskQuery,
    UserQuery,
):
    pass


@strawberry.type
class Mutation(
    # AuthMutation,
    # GroupMutation,
    # OrganizationMutation,
    # ProjectMutation,
    # RoleMutation,
    # TaskMutation,
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
)
