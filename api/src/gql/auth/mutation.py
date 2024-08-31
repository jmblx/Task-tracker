from uuid import UUID

import strawberry
from redis.asyncio import Redis
from strawberry import Info

from auth.reset_pwd_utils import set_new_pwd
from db.utils import get_user_by_id
from deps.cont import container
from google_auth.andoroid_auth import google_register
from gql.gql_types import UserType, GoogleRegDTO
from myredis.utils import get_user_id_from_reset_pwd_token


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def change_password(
        self, new_password: str, change_password_token: str
    ) -> bool:
        async with container() as ioc:
            redis = await ioc.get(Redis)
            user_id = await get_user_id_from_reset_pwd_token(
                redis, change_password_token
            )
        user = await get_user_by_id(user_id)
        await set_new_pwd(user, new_password)
        return True

    @strawberry.mutation
    async def confirm_account(self, info: Info, user_id: UUID) -> UserType:
        pass

    @strawberry.mutation
    @google_register
    async def google_register(
        self, info: Info, data: GoogleRegDTO
    ) -> UserType:
        pass
