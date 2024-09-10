from dishka import Provider, Scope, provide
from nats.aio.client import Client
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWTSettings
from domain.entities.user.models import User
from domain.repositories.user_repo import BaseRepository
from domain.services.auth.reset_pwd_service import ResetPwdService
from domain.services.entity_service import EntityService
from domain.services.user.service import UserServiceInterface
from infrastructure.services.user.service_impl import UserServiceImpl
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)
from infrastructure.services.auth.auth_service import AuthServiceImpl
from infrastructure.services.auth.jwt_service import JWTServiceImpl
from infrastructure.services.auth.reset_pwd_service import ResetPwdServiceImpl
from infrastructure.services.entity_service_impl import EntityServiceImpl
from infrastructure.services.security.pwd_service import HashServiceImpl
from infrastructure.services.validation.user import RegUserValidationService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=EntityService[User])
    def provide_entity_service(
        self, base_repo: BaseRepository[User]
    ) -> EntityService[User]:
        return EntityServiceImpl(base_repo)

    @provide(scope=Scope.REQUEST, provides=UserServiceInterface)
    def provide_user_service(
        self, entity_service: EntityService[User]
    ) -> UserServiceInterface:
        return UserServiceImpl(entity_service)

    @provide(scope=Scope.REQUEST, provides=NotifyServiceImpl)
    def provide_notify_service(self, nats_client: Client) -> NotifyServiceImpl:
        return NotifyServiceImpl(nats_client)

    @provide(scope=Scope.REQUEST, provides=HashServiceImpl)
    def provide_hash_service(self) -> HashServiceImpl:
        return HashServiceImpl()

    @provide(scope=Scope.REQUEST, provides=RegUserValidationService)
    def provide_validation_service(self) -> RegUserValidationService:
        return RegUserValidationService()

    @provide(scope=Scope.APP, provides=JWTServiceImpl)
    def provide_jwt_service(
        self, auth_settings: JWTSettings
    ) -> JWTServiceImpl:
        return JWTServiceImpl(auth_settings)

    @provide(scope=Scope.REQUEST, provides=AuthServiceImpl)
    def provide_auth_service(
        self,
        jwt_service: JWTServiceImpl,
        user_service: UserServiceInterface,
        redis: Redis,
        auth_settings: JWTSettings,
        hash_service: HashServiceImpl,
    ) -> AuthServiceImpl:
        return AuthServiceImpl(
            jwt_service, user_service, redis, auth_settings, hash_service
        )

    @provide(scope=Scope.REQUEST, provides=ResetPwdService)
    def provide_reset_pwd_service(
        self,
        redis: Redis,
    ):
        return ResetPwdServiceImpl(redis)
