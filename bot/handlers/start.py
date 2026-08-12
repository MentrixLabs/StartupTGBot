from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.kb.reply import main_actions_kb

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("token"):
        await message.answer(
            "👋 Добро пожаловать! Используйте кнопки меню для работы.",
            reply_markup=main_actions_kb  # импортируйте из bot.kb.reply
        )
        return

    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "У вас ещё нет активной сессии. Выберите действие:\n"
        "➡️ /register – создать новый аккаунт\n"
        "➡️ /login – войти в существующий"
    )