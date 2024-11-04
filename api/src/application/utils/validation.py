from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from strawberry import Info

from core.db.utils import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)


async def validate_permission(info: Info, entity: str, permission: str):
    try:
        token = info.context.get("auth_token").replace("Bearer ", "")
        user = await get_user_by_token(token)
    except (ExpiredSignatureError, DecodeError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)  # noqa: B904
    entity_permissions = user.role.permissions.get(entity)
    if permission not in entity_permissions:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)
