from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from auth.models import User
from db.utils import find_objs
from deps.cont import container


async def get_user_by_email(email: str) -> User:
    async with container() as di:
        session = await di.get(AsyncSession)
        query = select(User).where(User.email == email)
        res = await session.execute(query)
        return res.scalar()


async def find_user_by_search_data(find_data: dict) -> User:
    user = await find_objs(
        User, find_data, [load_only(User.id), load_only(User.email)]
    )
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user[0]
