from typing import Optional, List, Dict
import time
import logging
from uuid import UUID

import strawberry
from fastapi import Response
from fastapi.exceptions import HTTPException
from strawberry import Info
from strawberry.scalars import JSON

from auth.auth_helpers import authenticate_user, refresh_access_token
from auth.crud import get_user_by_email, get_user_by_id
from auth.helpers import create_access_token, create_refresh_token
from auth.models import User, Role, RefreshToken
from auth.utils import encode_jwt, validate_password, decode_jwt
from gql_types import (
    UserType,
    UserFindType,
    RoleType,
    RoleFindType,
    OrganizationType,
    OrganizationFindType,
    ProjectType,
    ProjectFindType,
    TaskType,
    TaskFindType,
    GroupType,
    GroupFindType,
    OrderByInput,
    UserAuthType,
)
from organization.models import Organization
from project.models import Project
from myredis.redis_config import get_redis
from myredis.utils import save_refresh_token_to_redis, token_to_redis
from task.models import Task, Group
from utils import insert_default
from graphql_utils import strawberry_field_with_params, find_objs, send_request_change_password, \
    find_user_by_search_data

logging.basicConfig(level=logging.INFO)


@strawberry.type
class Query:
    @strawberry.field
    async def request_change_password(
        self, info: strawberry.types.Info, find_data: UserFindType,
    ) -> bool:
        user = await find_user_by_search_data(find_data.__dict__)
        token = await send_request_change_password(user.email, info.context["nats_client"])
        async with get_redis() as redis:
            await token_to_redis(redis, user.id, token)
        return True

    @strawberry.field
    async def auth_user(self, info: strawberry.types.Info, auth_data: UserAuthType) -> JSON:
        user = await authenticate_user(auth_data.email, auth_data.password)
        access_token = create_access_token(user)
        fingerprint = info.context.get("fingerprint")

        async with get_redis() as redis:
            refresh_token_data = await create_refresh_token(user, fingerprint)
            await save_refresh_token_to_redis(redis, refresh_token_data)

        response = info.context["response"]
        response.set_cookie(
            key="refreshToken",
            value=refresh_token_data["token"],
            httponly=True,
            secure=False,
            samesite="lax",
        )

        return {"accessToken": access_token}

    @strawberry.field
    async def refresh(self, info: Info) -> JSON:
        refresh_token = info.context.get("refresh_token")
        fingerprint = info.context.get("fingerprint")

        if refresh_token is None:
            raise HTTPException(status_code=401)

        new_access_token = await refresh_access_token(refresh_token, fingerprint)
        return {"accessToken": new_access_token}

    @strawberry.field
    @strawberry_field_with_params(Role, RoleType, "getRole")
    async def get_role(
        self,
        info: Info,
        search_data: RoleFindType,
        order_by: Optional[OrderByInput] = None,
    ) -> Optional[List[RoleType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(User, UserType, "getUser")
    async def get_user(
        self,
        info: Info,
        search_data: UserFindType,
        order_by: Optional[OrderByInput] = None,
    ) -> Optional[List[UserType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Task, TaskType, "getTask")
    async def get_task(
        self,
        info: Info,
        search_data: TaskFindType,
        order_by: Optional[OrderByInput] = None,
    ) -> Optional[List[TaskType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Organization, OrganizationType, "getOrganization")
    async def get_organization(
        self,
        info: Info,
        search_data: OrganizationFindType,
        order_by: Optional[OrderByInput] = None,
    ) -> Optional[List[OrganizationType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Project, ProjectType, "getProject")
    async def get_project(
        self,
        info: Info,
        search_data: ProjectFindType,
        order_by: Optional[OrderByInput] = None,
    ) -> Optional[List[ProjectType]]:
        pass

    @strawberry.field
    @strawberry_field_with_params(Group, GroupType, "getGroup")
    async def get_group(
        self,
        info: Info,
        search_data: GroupFindType,
        order_by: Optional[OrderByInput] = None,
    ) -> Optional[List[GroupType]]:
        pass