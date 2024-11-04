import strawberry
from strawberry import Info

from application.usecases.role.create import CreateRoleAndReadUseCase
from application.usecases.role.delete import (
    DeleteAndReadRoleUseCase,
    DeleteRoleUseCase,
)
from application.usecases.role.update import UpdateRoleAndReadUseCase
from core.db.utils import get_selected_fields
from core.di.container import container
from presentation.gql.gql_types import OrderByInput
from presentation.gql.role.inputs import (
    RoleCreateType,
    RoleFindType,
    RoleUpdateType,
)
from presentation.gql.role.types import RoleType


@strawberry.type
class RoleMutation:
    @strawberry.mutation
    async def add_role(self, info: Info, data: RoleCreateType) -> RoleType:
        async with container() as ioc:
            interactor = await ioc.get(CreateRoleAndReadUseCase)
            selected_fields = get_selected_fields(info, "addRole")
            role = await interactor(data.__dict__, selected_fields)
            return RoleType.from_instance(role, selected_fields)

    @strawberry.mutation
    async def update_roles_with_response(
        self,
        info: Info,
        search_data: RoleFindType,
        data: RoleUpdateType,
        order_by: OrderByInput | None = None,
    ) -> list[RoleType]:
        async with container() as ioc:
            upd_data = {key: value for key, value in data.__dict__.items() if value is not None}
            interactor = await ioc.get(UpdateRoleAndReadUseCase)
            selected_fields = get_selected_fields(info, "updateRolesWithResponse")
            roles = await interactor(
                search_data.__dict__, upd_data, selected_fields,
                order_by.__dict__ if order_by is not None else None,
            )
            return [RoleType.from_instance(role, selected_fields) for role in roles]

    @strawberry.mutation
    async def delete_role(
        self,
        search_data: RoleFindType,
        full_delete: bool = False
    ) -> bool:
        async with container() as ioc:
            interactor = await ioc.get(DeleteRoleUseCase)
            await interactor(search_data.__dict__, full_delete)
            return True

    @strawberry.mutation
    async def delete_roles_with_response(
        self,
        info: Info,
        search_data: RoleFindType,
        order_by: OrderByInput | None = None,
        full_delete: bool = False,
    ) -> list[RoleType]:
        async with container() as ioc:
            interactor = await ioc.get(DeleteAndReadRoleUseCase)
            selected_fields = get_selected_fields(info, "deleteRolesWithResponse")
            roles = await interactor(
                search_data.__dict__, selected_fields,
                order_by.__dict__ if order_by is not None else None, full_delete
            )
            return [RoleType.from_instance(role, selected_fields) for role in roles]
