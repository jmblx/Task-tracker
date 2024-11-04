from dishka import Provider, Scope, provide

from domain.repositories.group.repo import GroupRepository
from domain.repositories.organization.repo import OrganizationRepository
from domain.repositories.project.repo import ProjectRepository
from domain.repositories.role.repo import RoleRepository
from domain.repositories.task.repo import TaskRepository
from domain.repositories.user.repo import UserRepository
from infrastructure.repositories.group.group_repo_impl import (
    GroupRepositoryImpl,
)
from infrastructure.repositories.organization.organization_repo_impl import OrganizationRepositoryImpl
from infrastructure.repositories.project.project_repo_impl import ProjectRepositoryImpl
from infrastructure.repositories.role.role_repo_impl import RoleRepositoryImpl
from infrastructure.repositories.task.task_repo_impl import TaskRepositoryImpl
from infrastructure.repositories.user.user_repo_impl import UserRepositoryImpl


class RepositoriesProvider(Provider):
    user_repo = provide(
        UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository
    )
    group_repo = provide(
        GroupRepositoryImpl, scope=Scope.REQUEST, provides=GroupRepository
    )
    organization_repo = provide(
        OrganizationRepositoryImpl, scope=Scope.REQUEST, provides=OrganizationRepository
    )
    project_repo = provide(
        ProjectRepositoryImpl, scope=Scope.REQUEST, provides=ProjectRepository
    )
    task_repo = provide(
        TaskRepositoryImpl, scope=Scope.REQUEST, provides=TaskRepository
    )
    role_repo = provide(
        RoleRepositoryImpl, scope=Scope.REQUEST, provides=RoleRepository
    )

