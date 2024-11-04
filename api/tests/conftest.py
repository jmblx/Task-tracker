import asyncio
import os
import sys
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm.exc import ObjectDeletedError

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)

from config import TEST_DATABASE_URI
from core.di.container import container
from domain.entities.user.models import User
from domain.services.security.pwd_service import HashService
from main import app

os.environ["USE_NULLPOOL"] = "true"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URI)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def async_engine() -> AsyncEngine:
    os.environ["DATABASE_URI"] = TEST_DATABASE_URI
    return create_async_engine(url=TEST_DATABASE_URI, echo=True)


@pytest.fixture(scope="session")
async def session_maker(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine)


@pytest.fixture(scope="function")
async def async_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[Any, Any]:
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def teardown_database(async_engine: AsyncEngine):
    """Удаление тестовой базы данных после завершения всех тестов."""
    yield

    async with async_engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))


@pytest.fixture
async def auth_headers(ac: AsyncClient) -> dict:
    """
    Фикстура для получения заголовков с авторизацией.
    """
    query = """
        query {
          authUser(authData: {
            email: "admin@admin.com"
            password: "admin"
          })
        }
    """
    headers = {"Fingerprint": "3ccc784000c0c0c11cab8508dffaa578"}

    response = await ac.post(
        "/graphql", headers=headers, json={"query": query}
    )

    assert response.status_code == 200
    data = response.json()
    access_token = data["data"]["authUser"]["accessToken"]
    headers["Authorization"] = f"Bearer {access_token}"
    return headers


@pytest.fixture(scope="function")
async def mock_user(async_session: AsyncSession) -> User:
    """
    Фикстура для создания тестового пользователя в базе данных с использованием ORM.
    """
    async with container() as ioc:
        hash_service = await ioc.get(HashService)

        user_mock = User(
            first_name="iojввввв",
            last_name="emвgyrвввв",
            role_id=4,
            email="aaaddd@b.b",
            hashed_password=hash_service.hash_password("b1b1b1b1"),
            is_active=True,
            is_verified=False,
        )

    async_session.add(user_mock)
    await async_session.commit()
    await async_session.refresh(user_mock)

    yield user_mock
    try:
        await async_session.delete(user_mock)
        await async_session.commit()
    except ObjectDeletedError:
        pass


@pytest.fixture
async def graphql_client(ac: AsyncClient, auth_headers: dict):
    """
    Фикстура для выполнения GraphQL-запросов с уже установленными заголовками.
    """

    class GraphQLClient:
        def __init__(self, client: AsyncClient, headers: dict):
            self.client = client
            self.headers = headers

        async def execute(self, query: str):
            """Выполняет GraphQL-запрос и возвращает ответ."""
            response = await self.client.post(
                "/graphql", headers=self.headers, json={"query": query}
            )
            return response

    return GraphQLClient(ac, auth_headers)
