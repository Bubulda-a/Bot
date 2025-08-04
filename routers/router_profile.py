from typing import Union

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import kb

router = Router(name="Общие функц")


class VideoStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_prompt = State()
    waiting_for_generation = State()


async def show_welcome_message(target: Union[Message, CallbackQuery]):
    text = (
        "👋 Привет! Это бот Google Veo 3 — генератор видео с помощью ИИ.\n"
        "📖 Инструкция — как пользоваться ботом (.....)\n"
        "💎 Осталось генераций: 0\n"
        "Что хочешь сгенерировать сегодня?"
    )

    if isinstance(target, CallbackQuery):
        await target.message.edit_text(
            text=text,
            reply_markup=kb.inline_kb1
        )
        await target.answer()
    else:
        await target.answer(
            text=text,
            reply_markup=kb.inline_kb1
        )


@router.message(Command("start"))
async def cmd_start(message: Message):
    await show_welcome_message(message)


@router.callback_query(F.data == "Back")
async def handle_back_button(callback: CallbackQuery):
    await show_welcome_message(callback)


@router.message(Command("help"))
async def send_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/start - Запустить бота\n"
        "/gen_vid - Сгенерировать видео\n"
        "/profile - Профиль\n"
        "/help - Эта справка"
    )


@router.callback_query(F.data == "generate_from_text")
async def handle_generate_from_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=f"💡 Введите описание видео:",
        reply_markup=kb.inline_kb2
    )

    await state.set_state(VideoStates.waiting_for_prompt)


@router.callback_query(F.data == "generate_from_photo")
async def handle_generate_from_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=f"📸 Отправьте фото исходник:",
        reply_markup=kb.inline_kb2
    )

    await state.set_state(VideoStates.waiting_for_photo)


@router.callback_query(F.data == "cash")
async def handle_generate_from_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=f"💳 Пополнить баланс 💰\n"
            "Нажмите кнопку ниже 👇",
        reply_markup=kb.inline_kb2
    )


@router.message()
async def handle_other_messages(message: types.Message):
    await message.answer("ℹ️ Используйте /help для списка команд")


@router.message(Command("help"))
async def send_help(message: Message):
    await message.reply("Вот что я могу:\n"
                        "/start - Начать общение\n"
                        "/help - Показать эту справку\n"
                        "/gen_vid - Сгенерировать видео\n"
                        "/login - Вход в аккаунт\n"
                        )
