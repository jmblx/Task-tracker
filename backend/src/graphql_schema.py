import strawberry
from strawberry.extensions import QueryDepthLimiter

from mutation import Mutation
from query import Query
from scalars import DateTime, Duration

schema = strawberry.Schema(query=Query, mutation=Mutation, types=[DateTime, Duration], extensions=[
        QueryDepthLimiter(max_depth=3),
    ],)
