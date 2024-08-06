import fastapi
from fastapi import Depends, Response
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from db.database import get_async_session

router = fastapi.APIRouter(prefix="/custom", tags=["custom-auth"])


@router.get("/email-confirmation/{token}")
async def processing_request(
    token: str,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    try:
        await session.execute(
            update(User)
            .where(User.email_confirmation_token == token)
            .values({"is_email_confirmed": True, "email_confirmation_token": None})
        )
        await session.commit()
    except Exception as e:
        print(e)
        response.status_code = HTTP_400_BAD_REQUEST
        return {"details": "invalid url for email confirmation"}


# @router.get("/auth-page")
# async def get_chat_page(request: Request):
#     return templates.TemplateResponse(
#         "registration.html", {"request": request}
#     )
