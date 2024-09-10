import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info
from fastapi import HTTPException
from starlette.responses import Response
from application.usecases.auth.change_pwd import RequestChangePasswordUseCase
from application.usecases.auth.cred_auth import AuthenticateUserUseCase
from application.usecases.auth.refresh_access_token import (
    RefreshAccessTokenUseCase,
)
from core.di.container import container
from presentation.gql.auth.inputs import UserAuthType, FullNameType


@strawberry.type
class AuthQuery:
    @strawberry.field
    async def request_change_password(
        self, email: str | None = None, full_name: FullNameType | None = None
    ) -> bool:
        if not email and not full_name:
            raise HTTPException(
                status_code=400, detail="Email or FullName is required"
            )
        async with container() as ioc:
            use_case = await ioc.get(RequestChangePasswordUseCase)
            return await use_case(
                email=email,
                full_name=full_name.to_dict() if not email else None,
            )

    @strawberry.field
    async def auth_user(self, info: Info, auth_data: UserAuthType) -> JSON:

        async with container() as ioc:
            use_case = await ioc.get(AuthenticateUserUseCase)

            response, access_token = await use_case(
                email=auth_data.email,
                plain_pwd=auth_data.password,
                fingerprint=info.context.get("fingerprint"),
                response=info.context["response"],
            )

        return access_token

    @strawberry.field
    async def refresh(self, info: Info) -> JSON:
        refresh_token = info.context.get("refresh_token")
        fingerprint = info.context.get("fingerprint")

        if refresh_token is None:
            raise HTTPException(status_code=401)

        async with container() as ioc:
            use_case = await ioc.get(RefreshAccessTokenUseCase)

            new_access_token = await use_case(
                refresh_token=refresh_token, fingerprint=fingerprint
            )

        return {"accessToken": new_access_token}
