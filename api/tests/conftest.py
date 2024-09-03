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

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)

from config import TEST_DATABASE_URI
from main import app

os.environ["USE_NULLPOOL"] = "true"


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
