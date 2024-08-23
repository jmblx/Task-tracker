from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


async def close_session(context: dict):
    # Закрываем сессию после завершения запроса
    db_session = context.get("db")
    if db_session:
        await db_session.close()


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Закрытие сессии после запроса
        context = request.state.context
        await close_session(context)
        return response
