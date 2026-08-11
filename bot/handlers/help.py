from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.kb.reply import main_actions_kb

router = Router()

@router.message(F.text == "❓ Помощь")
async def help_command(message: types.Message, state: FSMContext):
    await message.answer(
        text="❓ Помощь.",
        reply_markup=main_actions_kb,
    )
    await state.clear()
    