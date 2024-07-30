from sqlalchemy import update

from auth.models import User
from auth.utils import hash_password
from database import async_session_maker


async def set_new_pwd(user: User, new_pwd):
    async with async_session_maker() as session:
        hashed_pwd = hash_password(new_pwd)
        stmt = (update(User).where(User.id == user.id).values(hashed_password=hashed_pwd))
        await session.execute(stmt)
        await session.commit()
