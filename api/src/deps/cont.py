import logging
from collections.abc import AsyncIterable
import os

import redis.asyncio as aioredis
from dishka import Provider, Scope, make_async_container, provide
from nats.aio.client import Client
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import DatabaseConfig, NatsConfig, RedisConfig, AuthJWT

logger = logging.getLogger(__name__)


class NatsProvider(Provider):
    @provide(scope=Scope.APP, provides=NatsConfig)
    def provide_nats_config(self) -> NatsConfig:
        return NatsConfig.from_env()

    @provide(scope=Scope.APP, provides=Client)
    async def provide_nats_client(
        self, config: NatsConfig
    ) -> AsyncIterable[Client]:
        client = Client()
        await client.connect(servers=[config.uri])
        try:
            yield client
        finally:
            await client.close()


class DBProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig.from_env()

    @provide(scope=Scope.APP)
    def provide_engine(self, config: DatabaseConfig) -> AsyncEngine:
        pool_class = NullPool if os.getenv("USE_NULLPOOL", "false").lower() == "true" else None
        return create_async_engine(config.db_uri, poolclass=pool_class)

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session


class RedisProvider(Provider):
    @provide(scope=Scope.APP, provides=RedisConfig)
    def provide_redis_config(self) -> RedisConfig:
        return RedisConfig.from_env()

    @provide(scope=Scope.REQUEST, provides=aioredis.Redis)
    async def provide_redis(
        self, config: RedisConfig
    ) -> AsyncIterable[aioredis.Redis]:
        redis = await aioredis.from_url(
            config.rd_uri,
            encoding="utf8",
            decode_responses=True,
        )
        try:
            yield redis
        finally:
            await redis.close()


class AuthProvider(Provider):
    @provide(scope=Scope.APP, provides=AuthJWT)
    def provide_auth_settings(self) -> AuthJWT:
        return AuthJWT()


container = make_async_container(NatsProvider(), DBProvider(), RedisProvider(), AuthProvider())
