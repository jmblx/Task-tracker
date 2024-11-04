from fastapi import HTTPException

from domain.services.auth.auth_service import AuthService


class RefreshAccessTokenUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def __call__(self, refresh_token: str, fingerprint: str) -> str:
        token_data = await self.auth_service.get_refresh_token_data(
            refresh_token
        )

        if not token_data:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token"
            )

        if token_data.get("fingerprint") != fingerprint:
            raise HTTPException(status_code=401, detail="Invalid fingerprint")

        user = await self.auth_service.user_service.get_by_id(
            token_data.get("user_id"), {"id": {}, "email": {}, "role_id": {}}
        )
        return self.auth_service.create_access_token(user)
