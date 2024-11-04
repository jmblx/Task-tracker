from dishka import Provider, Scope, provide

from application.usecases.auth.change_pwd import RequestChangePasswordUseCase
from application.usecases.auth.cred_auth import AuthenticateUserUseCase
from application.usecases.auth.refresh_access_token import (
    RefreshAccessTokenUseCase,
)
from application.usecases.group.create import CreateGroupAndReadUseCase
from application.usecases.group.delete import (
    DeleteAndReadGroupUseCase,
    DeleteGroupUseCase,
)
from application.usecases.group.read import ReadGroupUseCase
from application.usecases.group.update import (
    UpdateGroupAndReadUseCase,
    UpdateGroupUseCase,
)
from application.usecases.organization.create import CreateOrganizationAndReadUseCase
from application.usecases.organization.delete import DeleteOrganizationUseCase, DeleteAndReadOrganizationUseCase
from application.usecases.organization.read import ReadOrganizationUseCase
from application.usecases.organization.update import UpdateOrganizationUseCase, UpdateOrganizationAndReadUseCase
from application.usecases.project.create import CreateProjectAndReadUseCase
from application.usecases.project.delete import DeleteProjectUseCase, DeleteAndReadProjectUseCase
from application.usecases.project.read import ReadProjectUseCase
from application.usecases.project.update import UpdateProjectUseCase, UpdateProjectAndReadUseCase
from application.usecases.role.create import CreateRoleAndReadUseCase
from application.usecases.role.delete import DeleteRoleUseCase, DeleteAndReadRoleUseCase
from application.usecases.role.read import ReadRoleUseCase
from application.usecases.role.update import UpdateRoleAndReadUseCase, UpdateRoleUseCase
from application.usecases.task.create import CreateTaskAndReadUseCase
from application.usecases.task.delete import DeleteTaskUseCase, DeleteAndReadTaskUseCase
from application.usecases.task.read import ReadTaskUseCase
from application.usecases.task.update import UpdateTaskUseCase, UpdateTaskAndReadUseCase
from application.usecases.user.delete import (
    DeleteAndReadUserUseCase,
    DeleteUserUseCase,
)
from application.usecases.user.read import ReadUserUseCase
from application.usecases.user.register import CreateUserAndReadUseCase
from application.usecases.user.set_image import SetAvatarUseCase
from application.usecases.user.update import (
    UpdateUserAndReadUseCase,
    UpdateUserUseCase,
)


class UseCaseProvider(Provider):
    create_user_and_read_use_case = provide(
        CreateUserAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateUserAndReadUseCase,
    )

    read_user_usecase = provide(
        ReadUserUseCase, scope=Scope.REQUEST, provides=ReadUserUseCase
    )

    authenticate_user_use_case = provide(
        AuthenticateUserUseCase,
        scope=Scope.REQUEST,
        provides=AuthenticateUserUseCase,
    )

    refresh_access_token_use_case = provide(
        RefreshAccessTokenUseCase,
        scope=Scope.REQUEST,
        provides=RefreshAccessTokenUseCase,
    )

    request_change_password_use_case = provide(
        RequestChangePasswordUseCase,
        scope=Scope.REQUEST,
        provides=RequestChangePasswordUseCase,
    )
    upd_user_uc = provide(
        UpdateUserUseCase,
        scope=Scope.REQUEST,
        provides=UpdateUserUseCase,
    )
    upd_and_read_user_uc = provide(
        UpdateUserAndReadUseCase,
        scope=Scope.REQUEST,
        provides=UpdateUserAndReadUseCase,
    )
    set_user_av_uc = provide(
        SetAvatarUseCase,
        scope=Scope.REQUEST,
        provides=SetAvatarUseCase,
    )
    del_user_uc = provide(
        DeleteUserUseCase, scope=Scope.REQUEST, provides=DeleteUserUseCase
    )
    del_and_read_user_uc = provide(
        DeleteAndReadUserUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadUserUseCase,
    )
    create_group_and_read_uc = provide(
        CreateGroupAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateGroupAndReadUseCase,
    )
    read_group_uc = provide(
        ReadGroupUseCase, scope=Scope.REQUEST, provides=ReadGroupUseCase
    )
    upd_group_uc = provide(
        UpdateGroupUseCase,
        scope=Scope.REQUEST,
        provides=UpdateGroupUseCase,
    )
    upd_and_read_group_uc = provide(
        UpdateGroupAndReadUseCase,
        scope=Scope.REQUEST,
        provides=UpdateGroupAndReadUseCase,
    )
    del_group_uc = provide(
        DeleteGroupUseCase, scope=Scope.REQUEST, provides=DeleteGroupUseCase
    )
    del_and_read_group_uc = provide(
        DeleteAndReadGroupUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadGroupUseCase,
    )
    # Organization use cases
    create_organization_uc = provide(
        CreateOrganizationAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateOrganizationAndReadUseCase,
    )
    read_organization_uc = provide(
        ReadOrganizationUseCase,
        scope=Scope.REQUEST,
        provides=ReadOrganizationUseCase,
    )
    upd_organization_uc = provide(
        UpdateOrganizationUseCase,
        scope=Scope.REQUEST,
        provides=UpdateOrganizationUseCase,
    )
    upd_and_read_organization_uc = provide(
        UpdateOrganizationAndReadUseCase,
        scope=Scope.REQUEST,
        provides=UpdateOrganizationAndReadUseCase,
    )
    del_organization_uc = provide(
        DeleteOrganizationUseCase,
        scope=Scope.REQUEST,
        provides=DeleteOrganizationUseCase,
    )
    del_and_read_organization_uc = provide(
        DeleteAndReadOrganizationUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadOrganizationUseCase,
    )

    # Project use cases
    create_project_uc = provide(
        CreateProjectAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateProjectAndReadUseCase,
    )
    read_project_uc = provide(
        ReadProjectUseCase,
        scope=Scope.REQUEST,
        provides=ReadProjectUseCase,
    )
    upd_project_uc = provide(
        UpdateProjectUseCase,
        scope=Scope.REQUEST,
        provides=UpdateProjectUseCase,
    )
    upd_and_read_project_uc = provide(
        UpdateProjectAndReadUseCase,
        scope=Scope.REQUEST,
        provides=UpdateProjectAndReadUseCase,
    )
    del_project_uc = provide(
        DeleteProjectUseCase,
        scope=Scope.REQUEST,
        provides=DeleteProjectUseCase,
    )
    del_and_read_project_uc = provide(
        DeleteAndReadProjectUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadProjectUseCase,
    )

    # Task use cases
    create_task_uc = provide(
        CreateTaskAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateTaskAndReadUseCase,
    )
    read_task_uc = provide(
        ReadTaskUseCase,
        scope=Scope.REQUEST,
        provides=ReadTaskUseCase,
    )
    upd_task_uc = provide(
        UpdateTaskUseCase,
        scope=Scope.REQUEST,
        provides=UpdateTaskUseCase,
    )
    upd_and_read_task_uc = provide(
        UpdateTaskAndReadUseCase,
        scope=Scope.REQUEST,
        provides=UpdateTaskAndReadUseCase,
    )
    del_task_uc = provide(
        DeleteTaskUseCase,
        scope=Scope.REQUEST,
        provides=DeleteTaskUseCase,
    )
    del_and_read_task_uc = provide(
        DeleteAndReadTaskUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadTaskUseCase,
    )
    create_role_uc = provide(
        CreateRoleAndReadUseCase,
        scope=Scope.REQUEST,
        provides=CreateRoleAndReadUseCase,
    )
    read_role_uc = provide(
        ReadRoleUseCase,
        scope=Scope.REQUEST,
        provides=ReadRoleUseCase,
    )
    upd_role_uc = provide(
        UpdateRoleUseCase,
        scope=Scope.REQUEST,
        provides=UpdateRoleUseCase,
    )
    upd_and_read_role_uc = provide(
        UpdateRoleAndReadUseCase,
        scope=Scope.REQUEST,
        provides=UpdateRoleAndReadUseCase,
    )
    del_role_uc = provide(
        DeleteRoleUseCase,
        scope=Scope.REQUEST,
        provides=DeleteRoleUseCase,
    )
    del_and_read_role_uc = provide(
        DeleteAndReadRoleUseCase,
        scope=Scope.REQUEST,
        provides=DeleteAndReadRoleUseCase,
    )
