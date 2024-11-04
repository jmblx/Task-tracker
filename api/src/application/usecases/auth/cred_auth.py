from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from config import JWTSettings
from domain.services.auth.auth_service import AuthService


class AuthenticateUserUseCase:
    def __init__(self, auth_service: AuthService, auth_settings: JWTSettings):
        self.auth_service = auth_service
        self.auth_settings = auth_settings

    async def __call__(
        self, fingerprint: str, email: str, plain_pwd: str
    ) -> dict[str, str]:
        if not fingerprint:
            raise HTTPException(
                HTTP_400_BAD_REQUEST, detail="Fingerprint is required"
            )

        user = await self.auth_service.authenticate_and_return_user(
            email, plain_pwd
        )

        access_token, refresh_token = await self.auth_service.create_tokens(
            user, fingerprint
        )

        return {"accessToken": access_token, "refreshToken": refresh_token}
