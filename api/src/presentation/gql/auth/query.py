import strawberry
from fastapi import HTTPException
from nats.aio.client import Client
from redis.asyncio import Redis
from strawberry import Info
from strawberry.scalars import JSON

from application.utils.auth_helpers import auth_user, refresh_access_token
from application.utils.helpers import authenticate
from application.utils.reset_pwd_utils import send_request_change_password
from config import AuthJWT
from core.di.container import container
from infrastructure.external_services.myredis.utils import token_to_redis
from infrastructure.repositories.user.crud import find_user_by_search_data
from presentation.gql.auth.inputs import UserAuthType
from presentation.gql.user.inputs import UserFindType


@strawberry.type
class AuthQuery:
    @strawberry.field
    async def request_change_password(
        self,
        find_data: UserFindType,
    ) -> bool:
        user = await find_user_by_search_data(find_data.__dict__)
        async with container() as ioc:
            nats_client = ioc.get(Client)
            redis = await ioc.get(Redis)

            token = await send_request_change_password(nats_client, user.email)

            await token_to_redis(redis, user.id, token)

        return True

    @strawberry.field
    async def auth_user(
        self, info: strawberry.types.Info, auth_data: UserAuthType
    ) -> JSON:
        user = await auth_user(auth_data.email, auth_data.password)

        async with container() as ioc:
            redis = await ioc.get(Redis)
            auth_settings = await ioc.get(AuthJWT)
            info.context["response"], access_token = await authenticate(
                redis, info, user, auth_settings
            )

        return access_token

    @strawberry.field
    async def refresh(self, info: Info) -> JSON:
        refresh_token = info.context.get("refresh_token")
        fingerprint = info.context.get("fingerprint")

        if refresh_token is None:
            raise HTTPException(status_code=401)

        new_access_token = await refresh_access_token(
            refresh_token, fingerprint
        )
        return {"accessToken": new_access_token}
