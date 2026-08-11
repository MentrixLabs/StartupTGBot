from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_article(product_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Отчёт",
                callback_data=f"report_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🪄 Генерация SEO",
                callback_data=f"generate_SEO_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🪄 Генерация инфографики",
                callback_data=f"generate_IG_{product_id}"
            )
        ]
    ])

cancel_delete_last_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Отмена', callback_data="delete_last_message")],
    ]
)