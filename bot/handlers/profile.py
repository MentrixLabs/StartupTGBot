from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.api_client import APIClient

router = Router()

@router.message(F.text == "✏️ Профиль")
async def profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get("token")
    if not token:
        await message.answer("⚠️ Сначала зарегистрируйтесь через /start")
        return

    api = APIClient(token)
    try:
        user = await api.get_me()
        text = (
            f"👤 *Профиль*\n"
            f"ID: {user['id']}\n"
            f"Имя: {user.get('full_name', 'Не указано')}\n"
            f"Email: {user['email']}\n"
            f"Username: {user['username']}"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка загрузки профиля: {str(e)}")