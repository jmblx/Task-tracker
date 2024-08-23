from fastapi import FastAPI
from fastapi.requests import Request
from strawberry.fastapi import GraphQLRouter

from gql.graphql_schema import schema, SQLAlchemySession
from main import get_default_context


async def mock_on_request_start(self):
    pass


# @pytest.fixture
# def mock_sqlalchemy_session(monkeypatch):
#     monkeypatch.setattr(SQLAlchemySession, "on_request_start", mock_on_request_start)
#
#     return SQLAlchemySession()


# @pytest.fixture(scope="session")
# def async_engine() -> AsyncEngine:
#     return create_async_engine(url=settings.test_db.test_database_url_postgresql, future=True, echo=True)
#
#
# @pytest.fixture(scope="session")
# def session_maker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
#     return async_sessionmaker(bind=async_engine)
#
#
# @pytest.fixture(scope='session')
# async def async_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[Any, Any]:
#     async with session_maker() as session:
#         yield session
