from dishka import Provider, Scope, provide

from domain.services.auth.auth_service import AuthService
from domain.services.auth.jwt_service import JWTService
from domain.services.auth.reset_pwd_service import ResetPwdService
from domain.services.group.group_interface import GroupServiceInterface
from domain.services.group.validation import GroupValidationService
from domain.services.notification.service import NotifyService
from domain.services.organization.organization_service_interface import OrganizationServiceInterface
from domain.services.organization.validation import OrganizationValidationService
from domain.services.project.access_policy import ProjectAccessPolicyInterface
from domain.services.project.project_service_interface import ProjectServiceInterface
from domain.services.project.validation import ProjectValidationService
from domain.services.role.role_service_interface import RoleServiceInterface
from domain.services.role.validation import RoleValidationService
from domain.services.security.pwd_service import HashService
from domain.services.storage.storage_service import StorageServiceInterface
from domain.services.task.task_service_interface import TaskServiceInterface
from domain.services.task.validation import TaskValidationService
from domain.services.user.access_policy import UserAccessPolicyInterface
from domain.services.user.user_service_interface import UserServiceInterface
from domain.services.user.validation import UserValidationService
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)
from infrastructure.external_services.storage.minio_service import MinIOService
from infrastructure.services.auth.auth_service import AuthServiceImpl
from infrastructure.services.auth.jwt_service import JWTServiceImpl
from infrastructure.services.auth.reset_pwd_service import ResetPwdServiceImpl
from infrastructure.services.group.entity_validator import (
    CreateGroupValidator,
)
from infrastructure.services.group.group_service import GroupServiceImpl
from infrastructure.services.organization.entity_validation import CreateOrganizationValidator
from infrastructure.services.organization.organization_service import OrganizationServiceImpl
from infrastructure.services.project.access_validation import ProjectAccessPolicy
from infrastructure.services.project.entity_validation import CreateProjectValidator
from infrastructure.services.project.project_service import ProjectServiceImpl
from infrastructure.services.role.entity_validator import CreateRoleValidator
from infrastructure.services.role.role_service import RoleServiceImpl
from infrastructure.services.security.pwd_service import HashServiceImpl
from infrastructure.services.task.entity_validator import CreateTaskValidator
from infrastructure.services.task.task_service import TaskServiceImpl
from infrastructure.services.user.access_validation import UserAccessPolicy
from infrastructure.services.user.entity_validation import RegUserValidationService
from infrastructure.services.user.user_service import UserServiceImpl


class ServiceProvider(Provider):

    # @provide(scope=Scope.REQUEST, provides=UserServiceInterface)
    # def provide_user_service(
    #     self, user_repo: UserRepository
    # ) -> UserServiceInterface:
    #     return UserServiceImpl(user_repo)
    user_service = provide(
        UserServiceImpl, scope=Scope.REQUEST, provides=UserServiceInterface
    )
    user_access_policy = provide(UserAccessPolicy, scope=Scope.REQUEST, provides=UserAccessPolicyInterface)
    notify_service = provide(
        NotifyServiceImpl, scope=Scope.REQUEST, provides=NotifyService
    )
    storage_service = provide(
        MinIOService, scope=Scope.REQUEST, provides=StorageServiceInterface
    )
    hash_service = provide(
        HashServiceImpl, scope=Scope.REQUEST, provides=HashService
    )
    reg_validation_service = provide(
        RegUserValidationService,
        scope=Scope.REQUEST,
        provides=UserValidationService,
    )
    jwt_service = provide(JWTServiceImpl, scope=Scope.APP, provides=JWTService)
    auth_service = provide(
        AuthServiceImpl, scope=Scope.REQUEST, provides=AuthService
    )
    reset_pwd_service = provide(
        ResetPwdServiceImpl, scope=Scope.REQUEST, provides=ResetPwdService
    )
    group_service = provide(
        GroupServiceImpl, scope=Scope.REQUEST, provides=GroupServiceInterface
    )
    group_validation_service = provide(
        CreateGroupValidator,
        scope=Scope.REQUEST,
        provides=GroupValidationService,
    )
    organization_service = provide(
        OrganizationServiceImpl, scope=Scope.REQUEST, provides=OrganizationServiceInterface
    )
    organization_validation_service = provide(
        CreateOrganizationValidator,
        scope=Scope.REQUEST,
        provides=OrganizationValidationService,
    )
    project_validation_service = provide(
        CreateProjectValidator,
        scope=Scope.REQUEST,
        provides=ProjectValidationService,
    )
    project_validation_policy = provide(ProjectAccessPolicy, scope=Scope.REQUEST, provides=ProjectAccessPolicyInterface)
    task_validation_service = provide(
        CreateTaskValidator,
        scope=Scope.REQUEST,
        provides=TaskValidationService,
    )
    role_validation_service = provide(
        CreateRoleValidator,
        scope=Scope.REQUEST,
        provides=RoleValidationService,
    )
    project_service = provide(
        ProjectServiceImpl, scope=Scope.REQUEST, provides=ProjectServiceInterface
    )
    task_service = provide(
        TaskServiceImpl, scope=Scope.REQUEST, provides=TaskServiceInterface
    )
    role_service = provide(
        RoleServiceImpl, scope=Scope.REQUEST, provides=RoleServiceInterface
    )
