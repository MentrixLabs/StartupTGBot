from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.states import RegisterStates, LoginStates
from bot.api_client import APIClient
from bot.kb.reply import main_actions_kb
import secrets

router = Router()

@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(RegisterStates.waiting_username)
    await message.answer(
        "📝 Регистрация нового аккаунта.\n"
        "Введите **имя пользователя** (username):",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(RegisterStates.waiting_username)
async def process_register_username(message: Message, state: FSMContext):
    username = message.text.strip()
    if not username:
        await message.answer("Имя не может быть пустым. Попробуйте снова.")
        return
    await state.update_data(username=username)
    await state.set_state(RegisterStates.waiting_email)
    await message.answer("Введите **email**:")

@router.message(RegisterStates.waiting_email)
async def process_register_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if not email or "@" not in email:
        await message.answer("Введите корректный email (содержит @).")
        return
    await state.update_data(email=email)
    await state.set_state(RegisterStates.waiting_password)
    await message.answer("Введите **пароль**:")

@router.message(RegisterStates.waiting_password)
async def process_register_password(message: Message, state: FSMContext):
    password = message.text.strip()
    if len(password) < 6:
        await message.answer("Пароль должен содержать минимум 6 символов.")
        return

    data = await state.get_data()
    username = data["username"]
    email = data["email"]

    api = APIClient()
    try:
        # 1. Регистрация
        await api.register(username, email, password)
        # 2. Логин (чтобы получить токен)
        login_data = await api.login(username, password)
        token = login_data["access_token"]

        # 3. Привязываем tg_id к пользователю (если бекенд поддерживает)
        await api.update_tg_id(message.from_user.id)

        # 4. Сохраняем токен в FSM
        await state.update_data(token=token)
        await state.clear()

        await message.answer(
            "✅ Регистрация успешна! Вы авторизированы.",
            reply_markup=main_actions_kb
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка регистрации: {str(e)}")
        await state.clear()

@router.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    # Проверяем, не авторизован ли уже
    data = await state.get_data()
    if data.get("token"):
        await message.answer("Вы уже авторизованы. Используйте /logout для выхода.")
        return

    await state.set_state(LoginStates.waiting_username)
    await message.answer(
        "🔐 Вход в аккаунт.\n"
        "Введите **имя пользователя**:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(LoginStates.waiting_username)
async def process_login_username(message: Message, state: FSMContext):
    username = message.text.strip()
    if not username:
        await message.answer("Имя не может быть пустым.")
        return
    await state.update_data(username=username)
    await state.set_state(LoginStates.waiting_password)
    await message.answer("Введите **пароль**:")

@router.message(LoginStates.waiting_password)
async def process_login_password(message: Message, state: FSMContext):
    password = message.text.strip()
    if not password:
        await message.answer("Пароль не может быть пустым.")
        return

    data = await state.get_data()
    username = data["username"]

    api = APIClient()
    try:
        login_data = await api.login(username, password)
        token = login_data["access_token"]

        # Привязываем tg_id, если его ещё нет
        await api.update_tg_id(token, message.from_user.id)

        await state.update_data(token=token)
        await state.clear()

        await message.answer(
            "✅ Вход выполнен!",
            reply_markup=main_actions_kb
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка входа: {str(e)}")
        await state.clear()