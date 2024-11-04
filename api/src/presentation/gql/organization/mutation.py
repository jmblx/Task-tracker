import strawberry
from strawberry import Info

from application.usecases.organization.create import CreateOrganizationAndReadUseCase
from application.usecases.organization.delete import (
    DeleteAndReadOrganizationUseCase,
    DeleteOrganizationUseCase,
)
from application.usecases.organization.update import (
    UpdateOrganizationAndReadUseCase,
    UpdateOrganizationUseCase,
)
from core.db.utils import get_selected_fields
from core.di.container import container
from presentation.gql.gql_types import OrderByInput
from presentation.gql.organization.inputs import (
    OrganizationCreateType,
    OrganizationFindType,
    OrganizationUpdateType,
)
from presentation.gql.organization.types import OrganizationType


@strawberry.type
class OrganizationMutation:
    @strawberry.mutation
    async def add_organization(self, info: Info, data: OrganizationCreateType) -> OrganizationType:
        async with container() as ioc:
            interactor = await ioc.get(CreateOrganizationAndReadUseCase)
            selected_fields = get_selected_fields(info, "addOrganization")
            organization = await interactor(data.__dict__, selected_fields)
            return OrganizationType.from_instance(organization, selected_fields)

    @strawberry.mutation
    async def update_organizations_with_response(
        self,
        info: Info,
        search_data: OrganizationFindType,
        data: OrganizationUpdateType,
        order_by: OrderByInput | None = None,
    ) -> list[OrganizationType]:
        async with container() as ioc:
            upd_data = {key: value for key, value in data.__dict__.items() if value is not None}
            interactor = await ioc.get(UpdateOrganizationAndReadUseCase)
            selected_fields = get_selected_fields(info, "updateOrganizationsWithResponse")
            organizations = await interactor(
                search_data.__dict__, upd_data, selected_fields,
                order_by.__dict__ if order_by is not None else None,
            )
            return [OrganizationType.from_instance(org, selected_fields) for org in organizations]

    @strawberry.mutation
    async def update_organizations(
        self,
        search_data: OrganizationFindType,
        data: OrganizationUpdateType,
    ) -> bool:
        async with container() as ioc:
            upd_data = {key: value for key, value in data.__dict__.items() if value is not None}
            interactor = await ioc.get(UpdateOrganizationUseCase)
            await interactor(search_data.__dict__, upd_data)
            return True

    @strawberry.mutation
    async def delete_organization(
        self,
        search_data: OrganizationFindType,
        full_delete: bool = False
    ) -> bool:
        async with container() as ioc:
            interactor = await ioc.get(DeleteOrganizationUseCase)
            await interactor(search_data.__dict__, full_delete)
            return True

    @strawberry.mutation
    async def delete_organizations_with_response(
        self,
        info: Info,
        search_data: OrganizationFindType,
        order_by: OrderByInput | None = None,
        full_delete: bool = False,
    ) -> list[OrganizationType]:
        async with container() as ioc:
            interactor = await ioc.get(DeleteAndReadOrganizationUseCase)
            selected_fields = get_selected_fields(info, "deleteOrganizationsWithResponse")
            organizations = await interactor(
                search_data.__dict__, selected_fields,
                order_by.__dict__ if order_by is not None else None, full_delete
            )
            return [OrganizationType.from_instance(org, selected_fields) for org in organizations]