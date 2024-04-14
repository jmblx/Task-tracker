import asyncio
import json
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiokafka import AIOKafkaConsumer
from dotenv import find_dotenv, load_dotenv

import config
from redis_config import RedisSession

load_dotenv(find_dotenv())
from kbds.reply import get_settings_keyboard
from handlers.auth import user_private_router as auth_router

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ["message, edited_message"]

bot_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(default=bot_properties, token=os.getenv("TOKEN"))
bot.my_admins_list = []

storage = MemoryStorage()
# При создании Dispatcher передайте storage:
dp = Dispatcher(storage=storage)

dp.include_router(auth_router)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        """
Конечно, я могу помочь украсить сообщение смайликами и дать совет по использованию стикеров в aiogram для приветствия пользователей. Вот как можно оформить ваше сообщение:

"Привет! 👋 После входа в аккаунт (данные те же, что и на сайте нашего трекера), я буду оповещать тебя о начале твоих задач 🚀 и о задачах, подходящих к концу по дате 📅 или оставшемуся времени ⏳!"
        """,
        reply_markup=get_settings_keyboard(),
    )


async def consume() -> None:
    consumer = AIOKafkaConsumer(
        config.CONSUME_TOPIC,
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            messages = json.loads(msg.value)
            for telegram_id, serialized in messages.items():
                if serialized.get("task_type") == "new_task":
                    message = (
                        f"Привет, {serialized['first_name']}! 🌟\n\n"
                        f"Тебе назначена новая задача:\n"
                        f"<b>{serialized['task_name']}</b>\n"
                        f"Описание: {serialized['task_description']}\n"
                        f"Группа задачи: {serialized['task_group_name']}\n"
                        f"Начало: {serialized['task_start_time']}\n"
                        f"Окончание: {serialized['task_end_time']}\n"
                        f"Длительность: {serialized['task_duration']} часов.\n"
                    )
                elif serialized.get("task_type") == "deadline_approaching":
                    message = (
                        f"⚠️ Внимание, {serialized['first_name']}!\n\n"
                        f"Срок выполнения задачи <b>{serialized['task_name']}</b> скоро истекает!\n"
                        f"Убедись, что все идет по плану. Осталось не так много времени.\n"
                    )
                elif serialized.get("task_type") == "task_started_no_activity":
                    message = (
                        f"⏳ {serialized['first_name']}, кажется ты еще не начал работу над задачей <b>{serialized['task_name']}</b>, которая уже началась!\n"
                        f"Пожалуйста, начни выполнение как можно скорее и обрати внимание на сроки.\n"
                    )

                if message:
                    await bot.send_message(chat_id=int(telegram_id), text=message, parse_mode="HTML")
    finally:
        await consumer.stop()



async def on_startup(bot):

    # run_param = False
    # if run_param:
    #     await drop_db()
    #
    # await create_db()
    print('')


async def on_shutdown(bot):
    # await drop_db()
    print("")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(RedisSession(os.getenv("REDIS_PATH", "redis://localhost")))
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    polling = asyncio.create_task(dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES))
    consuming = asyncio.create_task(consume())
    await asyncio.gather(polling, consuming)


if __name__ == "__main__":
    asyncio.run(main())
