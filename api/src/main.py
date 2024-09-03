import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request

# from logstash import TCPLogstashHandler
# from logstash import TCPLogstashHandler
# from starlette_exporter import PrometheusMiddleware, handle_metrics
from strawberry.fastapi import GraphQLRouter

import core.db.logs  # noqa: F401
from core.middlewares.middleware_utils import form_state
from presentation.gql.graphql_schema import schema
from presentation.routers.custom_auth_router import router as auth_router

# from auth.jwt_auth import router as jwt_router
from presentation.routers.router import router as speech_task_router

app = FastAPI(title="requests proceed API")


logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)

# logstash_handler = TCPLogstashHandler("logstash", 50000)
# logger.addHandler(logstash_handler)

app.include_router(auth_router)
app.include_router(speech_task_router)


@app.middleware("http")
async def add_auth_token_to_context(request: Request, call_next):
    request = form_state(
        request,
        {"authorization": "auth_token", "fingerprint": "fingerprint"},
        {"refreshToken": "refresh_token"},
    )
    return await call_next(request)


def get_default_context(request: Request) -> dict:
    return {
        "auth_token": request.state.auth_token,
        "refresh_token": request.state.refresh_token,
        "fingerprint": request.state.fingerprint,
        # "nats_client": nats_client,
    }


async def get_context(request: Request) -> dict:
    context = get_default_context(request)
    logger.info("request context: %s", context)
    return context


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

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
