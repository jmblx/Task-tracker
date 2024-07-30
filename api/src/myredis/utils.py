import logging
from datetime import datetime, timedelta
from uuid import UUID

from redis import asyncio as aioredis

from config import AuthJWT, settings

logging.basicConfig(level=logging.INFO)


async def save_refresh_token_to_redis(
    redis: aioredis.Redis, refresh_token_data: dict
) -> None:
    jti = str(refresh_token_data.pop("jti"))
    user_id = refresh_token_data["user_id"]
    fingerprint = refresh_token_data["fingerprint"]
    created_at = datetime.fromisoformat(refresh_token_data["created_at"]).timestamp()

    existing_jti = await redis.get(f"refresh_token_index:{user_id}:{fingerprint}")
    if existing_jti:
        logging.info(f"Found existing token with jti: {existing_jti}")
        await redis.delete(f"refresh_token:{existing_jti}")
        await redis.zrem(f"refresh_tokens:{user_id}", existing_jti)
    else:
        logging.info(
            f"No existing token found for user_id: {user_id} and fingerprint: {fingerprint}"
        )

    await redis.hset(f"refresh_token:{jti}", mapping=refresh_token_data)
    await redis.set(f"refresh_token_index:{user_id}:{fingerprint}", jti)
    logging.info(f"Saved new token with jti: {jti}")

    await redis.zadd(f"refresh_tokens:{user_id}", {jti: created_at})

    num_tokens = await redis.zcard(f"refresh_tokens:{user_id}")
    if num_tokens > settings.auth_jwt.refresh_token_by_user_limit:
        oldest_jti_list = await redis.zrange(f"refresh_tokens:{user_id}", 0, 0)
        if oldest_jti_list:
            oldest_jti = oldest_jti_list[0]
            logging.info(f"Removing oldest token with jti: {oldest_jti}")
            await redis.zrem(f"refresh_tokens:{user_id}", oldest_jti)
            await redis.delete(f"refresh_token:{oldest_jti}")
    else:
        logging.info(
            f"Number of tokens for user_id {user_id} is within limit: {num_tokens}"
        )


async def token_to_redis(redis: aioredis.Redis, user_id: UUID, token: str):
    await redis.set(f"reset_password:{token}", str(user_id), ex=timedelta(minutes=15))


async def get_user_id_from_reset_pwd_token(redis: aioredis.Redis, token: str) -> UUID:
    return UUID(await redis.get(f"reset_password:{token}"))