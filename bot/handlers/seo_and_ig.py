from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.api_client import APIClient

router = Router()

@router.callback_query(F.data.startswith("generate_SEO_"))
async def handle_generate_seo(callback: types.CallbackQuery, state: FSMContext):
    goods_id = int(callback.data.split("_")[2])
    data = await state.get_data()
    token = data.get("token")
    if not token:
        await callback.answer("⚠️ Сначала зарегистрируйтесь", show_alert=True)
        return

    await callback.answer("⏳ Генерирую SEO...", show_alert=False)

    api = APIClient(token)
    try:
        seo_result = await api.generate_seo(goods_id)
        text = (
            f"🪄 *Сгенерированное SEO:*\n\n"
            f"*Заголовок:* {seo_result['title']}\n"
            f"*Описание:* {seo_result['description']}\n"
            f"*Ключевые слова:* {', '.join(seo_result['keywords'])}"
        )
        await callback.message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка генерации SEO: {str(e)}")

@router.callback_query(F.data.startswith("generate_IG_"))
async def handle_generate_ig(callback: types.CallbackQuery, state: FSMContext):
    # Если есть эндпоинт для инфографики, используйте его.
    # Пока заглушка.
    await callback.answer("🖼️ Генерация инфографики пока недоступна", show_alert=True)