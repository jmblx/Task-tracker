from collections.abc import AsyncIterable

import redis.asyncio as aioredis
from dishka import Provider, Scope, provide

from config import RedisConfig


class RedisProvider(Provider):
    @provide(scope=Scope.APP, provides=RedisConfig)
    def provide_redis_config(self) -> RedisConfig:
        return RedisConfig.from_env()

    @provide(scope=Scope.REQUEST, provides=aioredis.Redis)
    async def provide_redis(
        self, config: RedisConfig
    ) -> AsyncIterable[aioredis.Redis]:
        redis = await aioredis.from_url(
            config.rd_uri, encoding="utf8", decode_responses=True
        )
        try:
            yield redis
        finally:
            await redis.close()
