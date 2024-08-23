from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from strawberry.extensions import Extension

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# Ссылка на базу данных для создания сессий
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
Base = declarative_base()


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class SQLAlchemySession(Extension):
    async def on_request_start(self):
        # Получаем сессию и сохраняем её в контексте запроса
        self.execution_context.context["db"] = await anext(get_async_session())

    async def on_request_end(self):
        # Закрываем сессию после завершения запроса
        db_session = self.execution_context.context.get("db")
        if db_session:
            await db_session.close()
