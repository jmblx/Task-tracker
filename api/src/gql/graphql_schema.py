import strawberry
from strawberry.extensions import QueryDepthLimiter, Extension

from db.database import get_async_session, async_session_maker
from gql.mutation import Mutation
from gql.query import Query
from gql.scalars import DateTime, Duration


class SQLAlchemySession(Extension):
    async def on_request_start(self):
        self.execution_context.context["db"] = async_session_maker()

    async def on_request_end(self):
        # Закрываем сессию после завершения запроса
        db_session = self.execution_context.context.get("db")
        if db_session:
            await db_session.close()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    types=[DateTime, Duration],
    extensions=[QueryDepthLimiter(max_depth=3), SQLAlchemySession],
)
