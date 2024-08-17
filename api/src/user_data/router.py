from uuid import UUID

import fastapi
from fastapi import Depends, Response
from fastapi.responses import FileResponse
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from auth.models import Role, User
from auth.schemas import RoleSchema
from db.database import get_async_session
from user_data.schemas import LinkTG

router = fastapi.APIRouter(prefix="/profile", tags=["user-profile"])


@router.get("/image/{user_id}")
async def get_image(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    user = await session.get(User, user_id)
    return FileResponse(user.pathfile)


@router.post("/add-role")
async def add_role(
    role: RoleSchema,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    stmt = insert(Role).values(**role.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/link/tg/")
async def link_tg(
    data: LinkTG,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        stmt = (
            update(User)
            .where(User.email == data.user_email)
            .values({"tg_id": str(data.tg_id)})
        )
        await session.execute(stmt)
        await session.commit()
        user = (
            await session.execute(
                select(User.id).where(User.email == data.user_email)
            )
        ).scalar()
    except IntegrityError:
        response.status_code = HTTP_404_NOT_FOUND
        return {"response": "произошла ошибка"}
    else:
        return {"response": user}
