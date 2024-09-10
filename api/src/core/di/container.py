from dishka import make_async_container
from core.di.providers.db import DBProvider
from core.di.providers.nats_provider import NatsProvider
from core.di.providers.redis_provider import RedisProvider
from core.di.providers.repositories import RepositoriesProvider
from core.di.providers.services import ServiceProvider
from core.di.providers.settings import SettingsProvider
from core.di.providers.usecases import UseCaseProvider

container = make_async_container(
    NatsProvider(),
    DBProvider(),
    RedisProvider(),
    RepositoriesProvider(),
    ServiceProvider(),
    SettingsProvider(),
    UseCaseProvider(),
)
