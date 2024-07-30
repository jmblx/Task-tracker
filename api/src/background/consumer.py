# consumer.py
from faststream import FastStream
from faststream
from email.message import EmailMessage
import aiosmtplib
import asyncio

from faststream.asyncapi.schema import Message

from config import BACKEND_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, NATS_URL

nats_url = "nats://localhost:4222"  # Замените на ваш NATS сервер

async def process_email_message(message: Message):
    email = message.data["email"]
    token = message.data["token"]

    email_message = EmailMessage()
    email_message["Subject"] = "Подтвердите регистрацию"
    email_message["From"] = SMTP_USER
    email_message["To"] = email
    email_content = f"""
        Здравствуйте! Если вы зарегистрировались в приложении task tracker,
        используя эту почту, то перейдите по следующей ссылке:
        {BACKEND_URL}/custom/email-confirmation/{token}
        чтобы подтвердить регистрацию.
    """
    email_message.set_content(email_content, subtype="html")

    try:
        await aiosmtplib.send(
            email_message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            use_tls=True,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    stream = FastStream(NATS_URL)

    stream.subscribe("email_queue", process_email_message)
    loop.run_until_complete(stream.start())
