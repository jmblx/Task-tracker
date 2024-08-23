import strawberry
from fastapi.exceptions import HTTPException
from strawberry import Info
from strawberry.scalars import JSON

from auth.auth_helpers import auth_user, refresh_access_token
from auth.crud import find_user_by_search_data
from auth.helpers import authenticate
from auth.models import Role, User
from auth.reset_pwd_utils import send_request_change_password
from gql.gql_types import (
    GroupFindType,
    GroupType,
    OrderByInput,
    OrganizationFindType,
    OrganizationType,
    ProjectFindType,
    ProjectType,
    RoleFindType,
    RoleType,
    TaskFindType,
    TaskType,
    UserAuthType,
    UserFindType,
    UserType,
)
from gql.graphql_utils import strawberry_read
from myredis.redis_config import get_redis
from myredis.utils import token_to_redis
from organization.models import Organization
from project.models import Project
from task.models import Group, Task

# logging.basicConfig(level=logging.INFO)


@strawberry.type
class Query:
    @strawberry.field
    async def request_change_password(
        self,
        info: strawberry.types.Info,
        find_data: UserFindType,
    ) -> bool:
        session = info.context.get("db")
        user = await find_user_by_search_data(find_data.__dict__, session)
        token = await send_request_change_password(
            user.email, info.context["nats_client"]
        )
        async with get_redis() as redis:
            await token_to_redis(redis, user.id, token)
        return True

    @strawberry.field
    async def auth_user(
        self, info: strawberry.types.Info, auth_data: UserAuthType
    ) -> JSON:
        user = await auth_user(auth_data.email, auth_data.password)
        info.context["response"], access_token = await authenticate(info, user)

        return access_token

    @strawberry.field
    async def refresh(self, info: Info) -> JSON:
        refresh_token = info.context.get("refresh_token")
        fingerprint = info.context.get("fingerprint")

        if refresh_token is None:
            raise HTTPException(status_code=401)

        new_access_token = await refresh_access_token(
            info.context["db"], refresh_token, fingerprint
        )
        return {"accessToken": new_access_token}

    @strawberry.field
    @strawberry_read(Role, RoleType, "getRole", need_validation=True)
    async def get_role(
        self,
        info: Info,
        search_data: RoleFindType,
        order_by: OrderByInput | None = None,
    ) -> list[RoleType] | None:
        pass

    @strawberry.field
    @strawberry_read(User, UserType, "getUser", need_validation=True)
    async def get_user(
        self,
        info: Info,
        search_data: UserFindType,
        order_by: OrderByInput | None = None,
    ) -> list[UserType] | None:
        pass

    @strawberry.field
    @strawberry_read(Task, TaskType, "getTask", need_validation=True)
    async def get_task(
        self,
        info: Info,
        search_data: TaskFindType,
        order_by: OrderByInput | None = None,
    ) -> list[TaskType] | None:
        pass

    @strawberry.field
    @strawberry_read(
        Organization, OrganizationType, "getOrganization", need_validation=True
    )
    async def get_organization(
        self,
        info: Info,
        search_data: OrganizationFindType,
        order_by: OrderByInput | None = None,
    ) -> list[OrganizationType] | None:
        pass

    @strawberry.field
    @strawberry_read(Project, ProjectType, "getProject", need_validation=True)
    async def get_project(
        self,
        info: Info,
        search_data: ProjectFindType,
        order_by: OrderByInput | None = None,
    ) -> list[ProjectType] | None:
        pass

    @strawberry.field
    @strawberry_read(Group, GroupType, "getGroup", need_validation=True)
    async def get_group(
        self,
        info: Info,
        search_data: GroupFindType,
        order_by: OrderByInput | None = None,
    ) -> list[GroupType] | None:
        pass
