from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.kb.reply import main_actions_kb
from config import settings
from bot.api_client import APIClient
import secrets

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    username = f"tg_{tg_id}"
    email = f"{tg_id}@telegram.bot"
    password = secrets.token_urlsafe(16)  # генерируем пароль

    # Пытаемся получить клиент из состояния
    data = await state.get_data()
    token = data.get("token")

    if not token:
        # Регистрируем и логинимся
        api = APIClient()
        try:
            # Пробуем зарегистрироваться
            try:
                await api.register(username, email, password)
            except Exception as e:
                # Возможно, пользователь уже существует – пробуем логин
                if "already exists" in str(e):
                    pass
                else:
                    raise
            # Логинимся
            login_data = await api.login(username, password)
            token = login_data["access_token"]
            await state.update_data(token=token)
        except Exception as e:
            await message.answer(f"❌ Ошибка авторизации: {str(e)}")
            return

    await message.answer(
        "👋 Добро пожаловать! Используйте кнопки меню для работы.",
        reply_markup=main_actions_kb
    )