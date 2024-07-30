import os

from dotenv import load_dotenv

load_dotenv()

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")

NATS_URL = os.environ.get("NATS_URL")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
