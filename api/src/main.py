from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nats.aio.client import Client

# from logstash import TCPLogstashHandler
from starlette.requests import Request
from starlette_exporter import PrometheusMiddleware, handle_metrics
from strawberry.fastapi import GraphQLRouter

import db.logs  # noqa: F401
from auth.custom_auth_router import router as auth_router
from config import NATS_URL
from gql.graphql_schema import schema
from middleware_utils import form_state

# from auth.jwt_auth import router as jwt_router
from speech_task.router import router as speech_task_router
from user_data.router import router as profile_router

app = FastAPI(title="requests proceed API")

nats_client = Client()


@app.on_event("startup")
async def startup_event():
    await nats_client.connect(servers=[NATS_URL])


@app.on_event("shutdown")
async def shutdown_event():
    await nats_client.close()


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(speech_task_router)


@app.middleware("http")
async def add_auth_token_to_context(request: Request, call_next):
    request = form_state(
        request,
        {"authorization": "auth_token", "fingerprint": "fingerprint"},
        {"refreshToken": "refresh_token"},
    )
    return await call_next(request)


async def get_context(request: Request) -> dict:
    return {
        "auth_token": request.state.auth_token,
        "refresh_token": request.state.refresh_token,
        "fingerprint": request.state.fingerprint,
        "nats_client": nats_client,
    }


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

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
