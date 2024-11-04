from uuid import UUID

import strawberry
from fastapi import HTTPException
from strawberry import Info
from strawberry.file_uploads import Upload

from application.dtos.set_image import ImageDTO
from application.usecases.user.delete import (
    DeleteAndReadUserUseCase,
    DeleteUserUseCase,
)
from application.usecases.user.register import CreateUserAndReadUseCase
from application.usecases.user.set_image import SetAvatarUseCase
from application.usecases.user.update import (
    UpdateUserAndReadUseCase,
    UpdateUserUseCase,
)
from core.db.utils import get_selected_fields

# from core.db.utils import full_delete_user
from core.di.container import container
from core.exceptions.user.delete import UserIsAdminOfOrgsException
from core.utils import get_selected_fields
from presentation.gql.gql_types import OrderByInput

# from domain.entities.user.models import User
# from presentation.gql.graphql_utils import (
#     strawberry_delete,
#     strawberry_update,
# )
from presentation.gql.user.inputs import (
    UserCreateType,
    UserFindType,
    UserUpdateType,
)
from presentation.gql.user.types import UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def add_user(self, info: Info, data: UserCreateType) -> UserType:
        async with container() as ioc:
            interactor = await ioc.get(CreateUserAndReadUseCase)
            selected_fields = get_selected_fields(info, "addUser")
            user = await interactor(data.__dict__, selected_fields)
            return UserType.from_instance(user, selected_fields)

    @strawberry.mutation
    async def update_users_with_response(
        self,
        info: Info,
        search_data: UserFindType,
        data: UserUpdateType,
        order_by: OrderByInput | None = None,
    ) -> list[UserType]:
        auth_token = info.context.get("auth_token")
        async with container() as ioc:
            upd_data = {
                key: value
                for key, value in data.__dict__.items()
                if value is not None
            }
            interactor = await ioc.get(UpdateUserAndReadUseCase)
            selected_fields = get_selected_fields(
                info, "updateUsersWithResponse"
            )
            users = await interactor(
                auth_token,
                search_data.__dict__,
                upd_data,
                selected_fields,
                order_by.__dict__ if order_by is not None else None,
            )
            return [
                UserType.from_instance(user, selected_fields) for user in users
            ]

    @strawberry.mutation
    async def update_users(
        self,
        info: Info,
        search_data: UserFindType,
        data: UserUpdateType,
    ) -> bool:
        auth_token = info.context.get("auth_token")
        async with container() as ioc:
            upd_data = {
                key: value
                for key, value in data.__dict__.items()
                if value is not None
            }
            interactor = await ioc.get(UpdateUserUseCase)
            await interactor(
                auth_token,
                search_data.__dict__,
                upd_data,
            )
            return True

    @strawberry.mutation
    async def set_user_avatar(
        self,
        user_id: UUID,
        file: Upload,
    ) -> str:
        content = await file.read()
        file_dto = ImageDTO(
            filename=file.filename,
            content=content,
            content_type=file.content_type,
        )
        async with container() as ioc:
            interactor = await ioc.get(SetAvatarUseCase)
            filepath = await interactor(user_id, file_dto)
        return filepath

    @strawberry.mutation
    async def delete_user(
        self, info: Info, search_data: UserFindType, full_delete: bool = False
    ) -> bool:
        auth_token = info.context.get("auth_token")
        async with container() as ioc:
            interactor = await ioc.get(DeleteUserUseCase)
            try:
                await interactor(
                    auth_token,
                    search_data.__dict__,
                    full_delete,
                )
            except UserIsAdminOfOrgsException as e:
                raise HTTPException(status_code=403, detail=str(e))
            return True

    @strawberry.mutation
    async def delete_users_with_response(
        self,
        info: Info,
        search_data: UserFindType,
        order_by: OrderByInput | None = None,
        full_delete: bool = False,
    ) -> list[UserType]:
        async with container() as ioc:
            interactor = await ioc.get(DeleteAndReadUserUseCase)
            selected_fields = get_selected_fields(
                info, "deleteUsersWithResponse"
            )
            try:
                users = await interactor(
                    search_data.__dict__,
                    selected_fields,
                    order_by.__dict__ if order_by is not None else None,
                    full_delete,
                )
            except UserIsAdminOfOrgsException as e:
                raise HTTPException(status_code=403, detail=str(e))
            return [
                UserType.from_instance(user, selected_fields) for user in users
            ]

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
