import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Загружаем скрытые данные из файла .env

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

PROJECT_DEBUG = os.environ.get("PROJECT_DEBUG")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
# DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
# DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
# DB_USER_TEST = os.environ.get("DB_USER_TEST")
# DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
#
# SENTRY_URL = os.environ.get("SENTRY_URL")
#
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
PRODUCE_TOPIC = os.environ.get("PRODUCE_TOPIC")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

NATS_URL = os.environ.get("NATS_URL", "nats://localhost:4222")

GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
# NATS_URL = "nats://localhost:4222"

API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS512"
    access_token_expire_minutes: int = 1500
    refresh_token_expire_days: int = 30
    refresh_token_by_user_limit: int = 5


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
