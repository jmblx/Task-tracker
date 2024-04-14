from aiogram import Router, F, types
from aiogram.filters import or_f, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from redis.asyncio.client import Redis

from utils import login, link

from app import bot

user_private_router = Router()


class Auth(StatesGroup):
    email = State()
    password = State()


@user_private_router.callback_query(or_f(
    F.data.startswith("auth")
))
async def auth(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите email аккаунта с сайта:")
    await state.set_state(Auth.email)
    await callback_query.answer()


@user_private_router.message(StateFilter('*'), Command("отмена"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены")


@user_private_router.message(Auth.email)
async def fix_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await state.set_state(Auth.password)
    await message.answer("Введите пароль к этому аккаунту сайта:")


@user_private_router.message(Auth.password)
async def fix_password(message: types.Message, state: FSMContext, redis: Redis):
    user_data = await state.get_data()
    user_data["password"] = message.text
    login_response = await login(user_data["email"], user_data["password"])
    token = login_response.get("access_token")
    if token:
        await redis.sadd(f"auth:{message.from_user.id}", token)
        link_response = await link(tg_id=message.from_user.id, email=str(user_data["email"]))
        import asyncio

        async def demo_messages():
            # Примеры импровизированных данных
            demo_data = {
                "new_task": {
                    "first_name": "Иван",
                    "task_name": "Разработка интерфейса",
                    "task_description": "Создание нового пользовательского интерфейса для нашего приложения",
                    "task_group_name": "Разработка ПО",
                    "task_start_time": "2022-04-14T08:00:00",
                    "task_end_time": "2022-04-20T17:00:00",
                    "task_duration": "48"
                },
                "deadline_approaching": {
                    "first_name": "Мария",
                    "task_name": "Отчет по продажам",
                    "task_description": "Подготовка ежемесячного отчета по продажам",
                    "task_group_name": "Отчетность",
                    "task_start_time": "2022-04-01T09:00:00",
                    "task_end_time": "2022-04-15T18:00:00",
                    "task_duration": "10"
                },
                "task_started_no_activity": {
                    "first_name": "Алексей",
                    "task_name": "Тестирование системы",
                    "task_description": "Проведение комплексного тестирования обновлений системы",
                    "task_group_name": "QA",
                    "task_start_time": "2022-04-10T10:00:00",
                    "task_end_time": "2022-04-13T16:00:00",
                    "task_duration": "24"
                }
            }

            # Имитация отправки сообщений для каждого типа задачи
            for task_type, data in demo_data.items():
                message = (
                    f"Привет, {data['first_name']}! 🌟\n\n"
                    f"Тебе назначена новая задача:\n"
                    f"<b>{data['task_name']}</b>\n"
                    f"Описание: {data['task_description']}\n"
                    f"Группа задачи: {data['task_group_name']}\n"
                    f"Начало: {data['task_start_time']}\n"
                    f"Окончание: {data['task_end_time']}\n"
                    f"Длительность: {data['task_duration']} часов.\n"
                )
                await bot.send_message(chat_id=12345678, text=message,
                                       parse_mode="HTML")  # Замените 12345678 на реальный ID пользователя
                await asyncio.sleep(5)  # Пауза в 5 секунд между сообщениями

        # Запуск демонстрации
        asyncio.run(demo_messages())

    else:
        await message.answer("Неверный логин и/или пароль")
    await state.clear()
