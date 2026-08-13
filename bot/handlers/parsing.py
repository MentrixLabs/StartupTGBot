from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.kb.reply import main_actions_kb
from bot.kb.inline import cancel_delete_last_keyboard
from bot.api_client import APIClient

router = Router()

class AddGoodsState(StatesGroup):
    GET_URL = State()

@router.message(F.text == "🧺 Добавить товар")
async def add_goods_start(message: Message, state: FSMContext):
    await message.answer("Введите ссылку на товар с Ozon:", reply_markup=cancel_delete_last_keyboard)
    await state.set_state(AddGoodsState.GET_URL)

@router.message(AddGoodsState.GET_URL, F.text)
async def add_goods_url(message: Message, state: FSMContext):
    url = message.text.strip()
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'

    data = await state.get_data()
    token = data.get("token")
    if not token:
        await message.answer("⚠️ Сначала зарегистрируйтесь через /start")
        await state.clear()
        return

    api = APIClient(token)
    try:
        new_goods = await api.create_goods(url)
    except Exception as e:
        await message.answer(f"❌ Ошибка добавления товара: {str(e)}")
        await state.clear()
        return

    await message.answer(
        f"✅ Товар *{new_goods['name']}* успешно добавлен!",
        parse_mode="Markdown",
        reply_markup=main_actions_kb
    )