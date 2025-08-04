from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎥Сгенерировать видео по тексту", callback_data="generate_from_text")],
    [InlineKeyboardButton(text="📸Сгенерировать видео по фото", callback_data="generate_from_photo")],
    [InlineKeyboardButton(text="💰Пополнить баланс", callback_data="cash")]
])
inline_kb2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙Вернуться", callback_data="Back")]])
