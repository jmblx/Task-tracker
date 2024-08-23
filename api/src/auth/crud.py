from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import load_only

from auth.models import User
from db.database import async_session_maker
from db.utils import find_objs


async def get_user_by_email(email: str, session) -> User:
    async with async_session_maker() as :
        query = select(User).where(User.email == email)
        res = await session.execute(query)
        return res.scalar()


async def find_user_by_search_data(find_data: dict, session) -> User:
    user = await find_objs(
        User, find_data, session, [load_only(User.id), load_only(User.email)]
    )
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user[0]
