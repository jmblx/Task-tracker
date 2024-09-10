from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from application.usecases.auth.change_pwd import RequestChangePasswordUseCase
from application.usecases.auth.cred_auth import AuthenticateUserUseCase
from application.usecases.auth.refresh_access_token import (
    RefreshAccessTokenUseCase,
)
from application.usecases.user.read import ReadUserUseCase
from config import JWTSettings
from domain.services.auth.reset_pwd_service import ResetPwdService
from domain.services.user.service import UserServiceInterface
from infrastructure.services.user.service_impl import UserServiceImpl
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)
from infrastructure.services.auth.auth_service import AuthServiceImpl
from infrastructure.services.security.pwd_service import HashServiceImpl
from infrastructure.services.validation.user import RegUserValidationService
from application.usecases.user.register import CreateUserAndReadUseCase


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=CreateUserAndReadUseCase)
    def provide_create_user_and_read_use_case(
        self,
        user_service: UserServiceInterface,
        notify_service: NotifyServiceImpl,
        hash_service: HashServiceImpl,
        validation_service: RegUserValidationService,
    ) -> CreateUserAndReadUseCase:
        return CreateUserAndReadUseCase(
            user_service=user_service,
            notify_service=notify_service,
            hash_service=hash_service,
            validation_service=validation_service,
        )

    @provide(scope=Scope.REQUEST, provides=ReadUserUseCase)
    def provide_read_user_use_case(
        self, user_service: UserServiceInterface
    ) -> ReadUserUseCase:
        return ReadUserUseCase(user_service)

    @provide(scope=Scope.REQUEST, provides=AuthenticateUserUseCase)
    def provide_authenticate_user_use_case(
        self,
        auth_service: AuthServiceImpl,
        auth_settings: JWTSettings,
    ) -> AuthenticateUserUseCase:
        return AuthenticateUserUseCase(auth_service, auth_settings)

    @provide(scope=Scope.REQUEST, provides=RefreshAccessTokenUseCase)
    def provide_refresh_access_token_use_case(
        self,
        auth_service: AuthServiceImpl,
    ) -> RefreshAccessTokenUseCase:
        return RefreshAccessTokenUseCase(auth_service)

    @provide(scope=Scope.REQUEST, provides=RequestChangePasswordUseCase)
    def provide_request_change_password_use_case(
        self,
        notify_service: NotifyServiceImpl,
        user_service: UserServiceInterface,
        reset_pwd_service: ResetPwdService,
    ) -> RequestChangePasswordUseCase:
        return RequestChangePasswordUseCase(
            notify_service, user_service, reset_pwd_service
        )
