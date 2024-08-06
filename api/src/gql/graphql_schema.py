import strawberry
from strawberry.extensions import QueryDepthLimiter

from gql.mutation import Mutation
from gql.query import Query
from gql.scalars import DateTime, Duration

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    types=[DateTime, Duration],
    extensions=[
        QueryDepthLimiter(max_depth=3),
    ],
)
