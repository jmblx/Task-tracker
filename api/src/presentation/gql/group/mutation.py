import strawberry
from strawberry import Info

from application.usecases.group.create import CreateGroupAndReadUseCase
from application.usecases.group.delete import (
    DeleteAndReadGroupUseCase,
    DeleteGroupUseCase,
)
from application.usecases.group.update import (
    UpdateGroupAndReadUseCase,
    UpdateGroupUseCase,
)
from core.db.utils import get_selected_fields
from core.di.container import container
from presentation.gql.gql_types import OrderByInput
from presentation.gql.group.inputs import (
    GroupCreateType,
    GroupFindType,
    GroupUpdateType,
)
from presentation.gql.group.query import GroupType


@strawberry.type
class GroupMutation:
    @strawberry.mutation
    async def add_group(self, info: Info, data: GroupCreateType) -> GroupType:
        async with container() as ioc:
            interactor = await ioc.get(CreateGroupAndReadUseCase)
            selected_fields = get_selected_fields(info, "addGroup")
            print(selected_fields)
            group = await interactor(data.__dict__, selected_fields)
            return GroupType.from_instance(group, selected_fields)

    @strawberry.mutation
    async def update_groups_with_response(
        self,
        info: Info,
        search_data: GroupFindType,
        data: GroupUpdateType,
        order_by: OrderByInput | None = None,
    ) -> list[GroupType]:
        async with container() as ioc:
            upd_data = {
                key: value
                for key, value in data.__dict__.items()
                if value is not None
            }
            interactor = await ioc.get(UpdateGroupAndReadUseCase)
            selected_fields = get_selected_fields(
                info, "updateGroupsWithResponse"
            )
            groups = await interactor(
                search_data.__dict__,
                upd_data,
                selected_fields,
                order_by.__dict__ if order_by is not None else None,
            )
            return [
                GroupType.from_instance(group, selected_fields)
                for group in groups
            ]

    @strawberry.mutation
    async def update_groups(
        self,
        search_data: GroupFindType,
        data: GroupUpdateType,
    ) -> bool:
        async with container() as ioc:
            upd_data = {
                key: value
                for key, value in data.__dict__.items()
                if value is not None
            }
            interactor = await ioc.get(UpdateGroupUseCase)
            await interactor(
                search_data.__dict__,
                upd_data,
            )
            return True

    @strawberry.mutation
    async def delete_group(
        self, search_data: GroupFindType, full_delete: bool = False
    ) -> bool:
        async with container() as ioc:
            interactor = await ioc.get(DeleteGroupUseCase)
            await interactor(
                search_data.__dict__,
                full_delete,
            )
            return True

    @strawberry.mutation
    async def delete_groups_with_response(
        self,
        info: Info,
        search_data: GroupFindType,
        order_by: OrderByInput | None = None,
        full_delete: bool = False,
    ) -> list[GroupType]:
        async with container() as ioc:
            interactor = await ioc.get(DeleteAndReadGroupUseCase)
            selected_fields = get_selected_fields(
                info, "deleteGroupsWithResponse"
            )
            groups = await interactor(
                search_data.__dict__,
                selected_fields,
                order_by.__dict__ if order_by is not None else None,
                full_delete,
            )
            return [
                GroupType.from_instance(group, selected_fields)
                for group in groups
            ]
