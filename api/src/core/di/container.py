import logging
import os
from collections.abc import AsyncIterable

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

from config import AuthJWT, DatabaseConfig, NatsConfig, RedisConfig
from domain.entities.user.models import User
from domain.services.user.service import UserService
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)
from infrastructure.repositories.user.repository import UserRepository
from infrastructure.services.entity_service_impl import EntityServiceImpl
from infrastructure.services.security.pwd_service import HashServiceImpl
from infrastructure.services.validation.user import RegValidationService

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
        pool_class = (
            NullPool
            if os.getenv("USE_NULLPOOL", "false").lower() == "true"
            else None
        )
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


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=UserRepository)
    def provide_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST, provides=UserService)
    def provide_user_service(self, session: AsyncSession) -> UserService:
        entity_service = EntityServiceImpl(User, session)
        return UserService(entity_service)

    @provide(scope=Scope.REQUEST, provides=NotifyServiceImpl)
    def provide_notify_service(self, nats_client: Client) -> NotifyServiceImpl:
        # Инжектируем NATS клиент в NotifyService
        return NotifyServiceImpl(nats_client)

    @provide(scope=Scope.REQUEST, provides=HashServiceImpl)
    def provide_hash_service(self) -> HashServiceImpl:
        # Предоставляем реализацию HashService
        return HashServiceImpl()

    @provide(scope=Scope.REQUEST, provides=RegValidationService)
    def provide_validation_service(self) -> RegValidationService:
        # Предоставляем реализацию ValidationService
        return RegValidationService()

    @provide(scope=Scope.REQUEST, provides=CreateUserAndReadUseCase)
    def provide_create_user_and_read_use_case(
        self,
        user_service: UserService,
        notify_service: NotifyServiceImpl,
        hash_service: HashServiceImpl,
        validation_service: RegValidationService,
    ) -> CreateUserAndReadUseCase:
        from application.usecases.user.register import CreateUserAndReadUseCase

        return CreateUserAndReadUseCase(
            user_service=user_service,
            notify_service=notify_service,
            hash_service=hash_service,
            validation_service=validation_service,
        )


container = make_async_container(
    NatsProvider(),
    DBProvider(),
    RedisProvider(),
    AuthProvider(),
    ServiceProvider(),
)
