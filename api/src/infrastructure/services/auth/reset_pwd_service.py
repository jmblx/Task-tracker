from datetime import timedelta
from uuid import UUID

from redis.asyncio import Redis

from domain.services.auth.reset_pwd_service import ResetPwdService


class ResetPwdServiceImpl(ResetPwdService):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_password_reset_token(
        self, user_id: UUID, token: str
    ) -> None:
        await self.redis.set(
            f"reset_password:{token}", str(user_id), ex=timedelta(minutes=15)
        )
