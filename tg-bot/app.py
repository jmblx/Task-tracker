import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types
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
    sticker_id = 'CAACAgIAAxkBAAEBFfde_sY4fiF8WUHjPp8w0PbwYrWnSgACGgADwDZPE4K7OvPbGCw_GQQ'
    await bot.send_sticker(message.chat.id, sticker_id)
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
                print(serialized, "ser")
                print(telegram_id, "tg_id")
                print(f'type {serialized.get("match_type")}')
                if serialized.get("match_type") == "1x1":
                    await bot.send_message(
                        chat_id=int(telegram_id),
                        text=serialized.get("match_result"),
                    )
                elif serialized.get("match_type") == "5x5":
                    print('res', serialized.get("match_result"))
                    if serialized.get("match_result") == "win":
                        message = (
                            f"<b>Поздравляем с победой!</b>\n\n"
                            f"<b>Матч:</b> {serialized['team_name']} против {serialized['opp_team_name']}\n"
                            f"<b>Счет:</b> {serialized['team_score']} - {serialized['opp_team_score']}\n"
                            f"<b>Ваша команда:</b> {', '.join(serialized['team_players'])}\n"
                            f"<b>Команда противника:</b> {', '.join(serialized['opp_team_players'])}\n"
                        )
                    elif serialized.get("match_result") == "lose":
                        message = (
                            f"<b>Не унывайте, впереди новые матчи!</b>\n\n"
                            f"<b>Матч:</b> {serialized['team_name']} против {serialized['opp_team_name']}\n"
                            f"<b>Счет:</b> {serialized['team_score']} - {serialized['opp_team_score']}\n"
                            f"<b>Ваша команда:</b> {', '.join(serialized['team_players'])}\n"
                            f"<b>Команда противника:</b> {', '.join(serialized['opp_team_players'])}\n"
                        )
                    else:
                        message = "<b>Произошла ошибка в обработке результатов матча.</b>"
                    print(message)
                    await bot.send_message(
                        chat_id=int(telegram_id),
                        text=message,
                        parse_mode="HTML"
                    )
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
