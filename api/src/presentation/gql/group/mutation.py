import strawberry
from strawberry import Info
from strawberry.scalars import JSON

from core.db.utils import full_delete_group
from domain.entities.group.models import Group
from presentation.gql.graphql_utils import (
    strawberry_delete,
    strawberry_insert,
    strawberry_update,
)
from presentation.gql.group.inputs import GroupCreateType, GroupUpdateType
from presentation.gql.group.query import GroupType


@strawberry.type
class GroupMutation:
    @strawberry.mutation
    @strawberry_insert(Group)
    async def add_group(self, info: Info, data: GroupCreateType) -> GroupType:
        pass

    @strawberry.mutation
    @strawberry_update(Group)
    async def update_group(
        self, info: Info, item_id: int, data: GroupUpdateType
    ) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_update(Group)
    async def update_group_with_response(
        self, info: Info, item_id: int, data: GroupUpdateType
    ) -> GroupType:
        pass

    @strawberry.mutation
    @strawberry_delete(Group)
    async def delete_group(self, info: Info, item_id: int) -> JSON:
        pass

    @strawberry.mutation
    @strawberry_delete(Group, del_func=full_delete_group)
    async def delete_group_with_response(
        self, info: Info, item_id: int
    ) -> GroupType:
        pass
