from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from auth.models import User
from auth.utils import decode_jwt
from database import async_session_maker


async def get_user_by_email(email: str) -> User:
    async with async_session_maker() as session:
        query = select(User).where(User.email == email)
        res = await session.execute(query)
        return res.scalar()


async def get_user_by_id(user_id: UUID, role: bool = False) -> User:
    async with async_session_maker() as session:
        if role:
            query = (
                select(User).where(User.id == user_id).options(joinedload(User.role))
            )
            user = (await session.execute(query)).unique().scalar()
        else:
            user = await session.get(User, user_id)
        return user


async def get_user_by_token(token: str) -> User:
    payload = decode_jwt(token)
    user = await get_user_by_id(payload.get("sub"), role=True)
    return user
