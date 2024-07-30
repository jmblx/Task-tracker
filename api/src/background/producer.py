
from faststream import FastStream
from faststream.message import Message
import asyncio

nats_url = "nats://localhost:4222"  # Замените на ваш NATS сервер

async def send_email_background(email: str, email_confirmation_token: str):
    message = {
        "email": email,
        "token": email_confirmation_token
    }
    await FastStream(nats_url).publish(Message("email_queue", message))

# Пример использования
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email_background("example@example.com", "confirmation_token"))
