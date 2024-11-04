from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from nats.aio.client import Client

from config import NatsConfig


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
