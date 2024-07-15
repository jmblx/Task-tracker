import os
import time

import redis.asyncio as aioredis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter

from auth.base_config import (
    auth_backend,
    fastapi_users,
    google_oauth_client,
)
from auth.custom_auth_router import router as auth_router
from auth.schemas import UserRead, UserCreate, UserUpdate
from database import get_async_session
from loader import UserLoader, RoleLoader, TaskLoader
from speech_task.router import router as speech_task_router
from config import SECRET_AUTH
from graphql_schema import schema
from user_data.router import router as profile_router
from integration.multiple_tasks import router as asana_router


import logging
from sqlalchemy.engine import Engine
from sqlalchemy import event


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Настройка логирования для SQLAlchemy
# @event.listens_for(Engine, "before_cursor_execute")
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     conn.info.setdefault('query_start_time', []).append(time.time())
#     logging.info("Start Query: %s" % statement)
#     logging.info("Parameters: %s" % parameters)
#
# @event.listens_for(Engine, "after_cursor_execute")
# def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     total = time.time() - conn.info['query_start_time'].pop(-1)
#     logging.info("Query Complete!")
#     logging.info("Total Time: %f" % total)
#
# @event.listens_for(Engine, "handle_error")
# def handle_error(context):
#     logging.error("An exception occurred: %s", context.original_exception)


app = FastAPI(title="requests proceed API")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET_AUTH,
        redirect_url=f"http://localhost:{os.getenv('PORT')}/auth/google/callback",
        is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_oauth_associate_router(
        google_oauth_client, UserRead, "SECRET"
    ),
    prefix="/auth/associate/google",
    tags=["auth"],
)

app.include_router(auth_router)
app.include_router(profile_router)
# app.include_router(asana_router)
app.include_router(speech_task_router)

async def get_context(
    session: AsyncSession = Depends(get_async_session)
):
    return {
        "db": session,
        "user_loader": UserLoader(session),
        "role_loader": RoleLoader(session),
        "task_loader": TaskLoader(session)
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.on_event("startup")
async def startup_event():
    # redis = aioredis.from_url(
    #     f"redis://{REDIS_HOST}:{REDIS_PORT}",
    #     encoding="utf8",
    #     decode_responses=True,
    # )
    pass
