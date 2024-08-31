import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Загружаем скрытые данные из файла .env

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")
TEST_DATABASE_URI = os.environ.get(
    "TEST_DATABASE_URI",
    f"postgresql+asyncpg://{DB_USER_TEST}:"
    f"{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}",
)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    f"postgresql+asyncpg://"
    f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


@dataclass(frozen=True)
class DatabaseConfig:
    db_uri: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        uri = os.getenv("DATABASE_URI", DATABASE_URI)

        if not uri:
            raise RuntimeError("Missing DATABASE_URI environment variable")

        return DatabaseConfig(uri)


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}"


@dataclass(frozen=True)
class RedisConfig:
    rd_uri: str

    @staticmethod
    def from_env() -> "RedisConfig":
        uri = os.environ.get("REDIS_URI", REDIS_URI)

        if not uri:
            raise RuntimeError("Missing REDIS_URI environment variable")

        return RedisConfig(uri)


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


class NatsConfig:
    def __init__(self, uri: str):
        self.uri = uri

    @staticmethod
    def from_env() -> "NatsConfig":
        return NatsConfig(uri=NATS_URL)


GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
# NATS_URL = "nats://localhost:4222"

YANDEX_PRIVATE_KEY = os.environ.get("YANDEX_PRIVATE_KEY")
SERVICE_ACCOUNT_ID = os.environ.get("SERVICE_ACCOUNT_ID")
KEY_ID = os.environ.get("KEY_ID")
FOLDER_ID = os.environ.get("FOLDER_ID")

API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")


class AuthJWT(BaseModel):
    private_key_path: Path = Path(__file__).parent.parent / "certs" / "jwt-private.pem"
    public_key_path: Path = Path(__file__).parent.parent / "certs" / "jwt-public.pem"
    algorithm: str = "RS512"
    access_token_expire_minutes: int = 1500
    refresh_token_expire_days: int = 30
    refresh_token_by_user_limit: int = 5

    _private_key: str = None
    _public_key: str = None

    def __post_init__(self):
        if self._private_key is None:
            self._private_key = self.private_key_path.read_text()
        if self._public_key is None:
            self._public_key = self.public_key_path.read_text()

    @property
    def private_key(self) -> str:
        if self._private_key is None:
            self._private_key = self.private_key_path.read_text()
        return self._private_key

    @property
    def public_key(self) -> str:
        if self._public_key is None:
            self._public_key = self.public_key_path.read_text()
        return self._public_key
