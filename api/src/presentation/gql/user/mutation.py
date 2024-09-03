import secrets
from uuid import UUID

import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from core.db.utils import full_delete_user
from core.utils import hash_user_pwd
from domain.entities.user.models import User
from presentation.gql.graphql_utils import (
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
)
from presentation.gql.user.inputs import UserCreateType, UserUpdateType
from presentation.gql.user.types import UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    @strawberry_insert(
        User,
        process_extra_db=hash_user_pwd,
        exc_fields=["password"],
        notify_kwargs={"email_confirmation_token": secrets.token_urlsafe(32)},
        notify_from_data_kwargs={"email": "email"},
        notify_subject="email.confirmation",
        validation=False,
    )
    async def add_user(self, info: Info, data: UserCreateType) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_update(User)
    async def update_user(
        self, info: Info, item_id: UUID, data: UserUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(User)
    async def update_user_with_response(
        self, info: Info, item_id: int, data: UserUpdateType
    ) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_delete(User)
    async def delete_user(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(User)
    async def delete_user_with_response(
        self, info: Info, item_id: UUID
    ) -> UserType:
        pass

    @strawberry.mutation
    @strawberry_delete(User, del_func=full_delete_user)
    async def full_delete_user(self, info: Info, item_id: UUID) -> UserType:
        pass
