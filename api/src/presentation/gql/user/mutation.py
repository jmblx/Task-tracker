import strawberry
from strawberry import Info

from application.dtos.user import UserCreateDTO
from application.usecases.user.register import CreateUserAndReadUseCase
from core.db.utils import get_selected_fields

# from core.db.utils import full_delete_user
from core.di.container import container
from core.utils import get_selected_fields

# from domain.entities.user.models import User
# from presentation.gql.graphql_utils import (
#     strawberry_delete,
#     strawberry_update,
# )
from presentation.gql.user.inputs import UserCreateType
from presentation.gql.user.types import UserType


@strawberry.type
class UserMutation:
    # @strawberry_insert(
    #     User,
    #     process_extra_db=hash_user_pwd,
    #     exc_fields=["password"],
    #     notify_kwargs={"email_confirmation_token": secrets.token_urlsafe(32)},
    #     notify_from_data_kwargs={"email": "email"},
    #     notify_subject="email.confirmation",
    #     validation=False,
    # )
    @strawberry.mutation
    async def add_user(self, info: Info, data: UserCreateType) -> UserType:
        # user_dto = UserCreateDTO(
        #     first_name=data.first_name,
        #     last_name=data.last_name,
        #     email=data.email,
        #     password=data.password,  # Пароль будет хэшироваться позже
        #     role_id=data.role_id,
        #     is_active=data.is_active if data.is_active is not None else True,
        #     is_verified=(
        #         data.is_verified if data.is_verified is not None else False
        #     ),
        #     pathfile=data.pathfile,
        #     tg_id=data.tg_id,
        #     tg_settings=data.tg_settings,
        #     github_name=data.github_name,
        # )
        async with container() as ioc:
            interactor = await ioc.get(CreateUserAndReadUseCase)
            selected_fields = get_selected_fields(info, "addUser")
            user = await interactor(data.__dict__, selected_fields)
            return UserType.from_instance(user, selected_fields)

    # @strawberry.mutation
    # @strawberry_update(User)
    # async def update_user(
    #     self, info: Info, item_id: UUID, data: UserUpdateType
    # ) -> JSON:
    #     pass
    #
    # @strawberry.mutation
    # @strawberry_update(User)
    # async def update_user_with_response(
    #     self, info: Info, item_id: int, data: UserUpdateType
    # ) -> UserType:
    #     pass
    #
    # @strawberry.mutation
    # @strawberry_delete(User)
    # async def delete_user(self, info: Info, item_id: int) -> JSON:
    #     pass
    #
    # @strawberry.mutation
    # @strawberry_delete(User)
    # async def delete_user_with_response(
    #     self, info: Info, item_id: UUID
    # ) -> UserType:
    #     pass
    #
    # @strawberry.mutation
    # @strawberry_delete(User, del_func=full_delete_user)
    # async def full_delete_user(self, info: Info, item_id: UUID) -> UserType:
    #     pass
