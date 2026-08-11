from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_actions_kb = ReplyKeyboardMarkup(
    keyboard=[
        [(KeyboardButton(text="📦 Товары")),(KeyboardButton(text="🧺 Добавить товар"))],
        [(KeyboardButton(text="✏️ Профиль")),(KeyboardButton(text="❓ Помощь"))],
    ],
    resize_keyboard=True,
)
