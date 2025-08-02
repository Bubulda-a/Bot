import kb
import time
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile
import requests
import os

VIDEO_API_TOKEN = os.getenv("VIDEO_API_KEY")
router = Router(name="Общие функции")

class VideoStates(StatesGroup):
    waiting_for_prompt = State()


@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply(f"🎥 Привет, {message.from_user.username} !Введите /help, чтобы узнать, что я умею.")


@router.message(Command("help"))
async def send_help(message: Message):
    await message.reply("Вот что я могу:\n"
                        "/start - Начать общение\n"
                        "/help - Показать эту справку\n"
                        "/gen_vid - Сгенерировать видео\n"
                        "/login - Вход в аккаунт\n"
                        )


async def generate_video(prompt: str):
    return "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"



@router.message(Command("gen_vid"))
async def cmd_veo(message: types.Message, state: FSMContext):
    await message.answer("💡 Введите описание видео:")
    await state.set_state(VideoStates.waiting_for_prompt)


@router.message(VideoStates.waiting_for_prompt, F.text)
async def process_prompt(message: Message, state: FSMContext):
    prompt = message.text

    if video_url := await generate_video(prompt):
        await message.answer_video(video_url, caption="Ваше видео готово!")
    else:
        await message.answer("❌ Ошибка генерации. Попробуйте другой запрос.")

    await state.clear()



@router.message()
async def handle_other_messages(message: types.Message):
    await message.answer("ℹ️ Для генерации видео используйте /gen_vid")


