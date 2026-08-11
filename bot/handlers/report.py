from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.api_client import APIClient

router = Router()

@router.callback_query(F.data.startswith("report_"))
async def handle_report(callback: types.CallbackQuery, state: FSMContext):
    goods_id = int(callback.data.split("_")[1])
    data = await state.get_data()
    token = data.get("token")
    if not token:
        await callback.answer("⚠️ Сначала зарегистрируйтесь", show_alert=True)
        return

    await callback.answer("⏳ Генерирую отчёт...", show_alert=False)

    api = APIClient(token)
    try:
        pdf_bytes = await api.generate_report(goods_id)
        # Отправляем PDF как документ
        await callback.message.answer_document(
            types.BufferedInputFile(pdf_bytes, filename=f"report_{goods_id}.pdf"),
            caption=f"📊 Отчёт по товару ID: {goods_id}"
        )
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка генерации отчёта: {str(e)}")
    await callback.answer()