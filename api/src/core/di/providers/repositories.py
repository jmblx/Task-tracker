from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user.models import User
from domain.repositories.user_repo import BaseRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=BaseRepository[User])
    def provide_user_repository(
        self, session: AsyncSession
    ) -> BaseRepository[User]:
        return BaseRepositoryImpl(User, session)
