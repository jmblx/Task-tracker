import logging
from email.message import EmailMessage
import aiosmtplib

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

subject_email_routing = {
    "confirmation": {
        "text": """
        Здравствуйте! Если вы зарегистрировались в приложении task tracker,
        используя эту почту, то перейдите по следующей ссылке:
        BACKEND_URL/custom/email-confirmation/email_confirmation_token
        чтобы подтвердить регистрацию.""",
        "subject": "Подтверждение почты",
    },
    "reset_password": {
        "text": """
        Здравствуйте! Кто-то пытается сменить пароль по этой почте,
        вот ссылка, по которой нужно перейти, чтобы сменить пароль:
        BACKEND_URL/custom/reset-password/token
        длительность ссылки = 15 минут
        если это не вы, то возможно к вашему аккаунту пытаются
        получить доступ злоумышленники.""",
        "subject": "Сброс пароля",
    },
}


def format_email(subject: str, **kwargs):
    routing_key = subject.split(".")[1]
    base = subject_email_routing.get(routing_key, None).get("text")
    email_subject = subject_email_routing.get(routing_key, None).get("subject")
    if base is None:
        raise ValueError(f"Unknown topic {subject}")
    for key, value in kwargs.items():
        base = base.replace(f"{key}", value)
    return base, email_subject


async def send_email(email: str, subject: str, **kwargs):
    email_content, email_subject = format_email(subject, **kwargs)
    logger.info(f"Sending email to {email}")
    message = EmailMessage()
    message["Subject"] = email_subject
    message["From"] = SMTP_USER
    message["To"] = email
    message.set_content(email_content, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            use_tls=True,
        )
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
