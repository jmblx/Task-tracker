import fastapi
from fastapi import HTTPException
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from auth.models import User

# from db.database import get_async_session
from deps.cont import container

router = fastapi.APIRouter(prefix="/custom", tags=["custom-auth"])


@router.get("/email-confirmation/{token}")
async def processing_request(
    token: str,
    # response: Response,
    # session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    try:
        async with container() as di:
            session = await di.get(AsyncSession)
        await session.execute(
            update(User)
            .where(User.email_confirmation_token == token)
            .values(
                {"is_email_confirmed": True, "email_confirmation_token": None}
            )
        )
        await session.commit()
    except NoResultFound as err:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=str(err)
        ) from err
    except (ExpiredSignatureError, DecodeError) as err:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from err
