from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.kb.inline import get_inline_article
from bot.api_client import APIClient

router = Router()

@router.message(F.text == "📦 Товары")
async def look_goods(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get("token")
    if not token:
        await message.answer("⚠️ Сначала зарегистрируйтесь через /start")
        return

    api = APIClient(token)
    try:
        goods = await api.get_goods(page=1, size=20)
    except Exception as e:
        await message.answer(f"❌ Ошибка загрузки товаров: {str(e)}")
        return

    if not goods:
        await message.answer("📭 У вас пока нет товаров. Добавьте через '🧺 Добавить товар'")
        return

    # Сохраняем список товаров в state (для быстрого доступа)
    products_map = {str(item["id"]): item["name"] for item in goods}
    await state.update_data(products_map=products_map)

    for item in goods:
        # Формируем сообщение
        text = (
            f"📦 *{item['name']}*\n"
            f"🏷 Категория: {item.get('category', 'Нет данных')}\n"
            f"💰 Цена: {item.get('price', 'Нет данных')} ₽\n"
            f"⭐ Рейтинг: {item.get('rating', '—')}\n"
            f"🆔 ID: {item['id']}"
        )
        await message.answer(
            text,
            parse_mode="Markdown",
            reply_markup=get_inline_article(str(item["id"]))
        )