import asyncio
import os
import kb
import requests
import time
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from keyboards import kb

load_dotenv()

router = Router(name="video_generation")


class VideoStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_prompt = State()
    waiting_for_generation = State()


async def start_video_generation(prompt: str, image_url: str = None) -> str:

    url = "https://api.aimlapi.com/v2/generate/video/minimax/generation"
    payload = {
        "model": "video-01",
        "prompt": prompt,
    }

    if image_url:
        payload["first_frame_image"] = image_url

    headers = {
        "Authorization": f"Bearer {os.getenv('VIDEO_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("generation_id")
    except Exception as e:
        print(f"Error starting generation: {e}")
        return None


async def check_video_status(generation_id: str) -> dict:

    url = "https://api.aimlapi.com/v2/generate/video/minimax/generation"
    params = {"generation_id": generation_id}
    headers = {
        "Authorization": f"Bearer {os.getenv('VIDEO_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error checking status: {e}")
        return None


async def wait_for_video_completion(generation_id: str, timeout: int = 300) -> str:

    start_time = time.time()
    while time.time() - start_time < timeout:
        status_data = await check_video_status(generation_id)
        if not status_data:
            return None

        status = status_data.get("status")
        if status == "completed":
            return status_data.get("video_url")
        elif status in ["failed", "cancelled"]:
            return None

        await asyncio.sleep(10)  # Проверяем каждые 10 секунд

    return None


@router.message(VideoStates.waiting_for_prompt, F.text)
async def process_prompt(message: Message, state: FSMContext):
    prompt = message.text
    await message.answer("⏳ Запускаю генерацию видео...")

    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Cheetah4.jpg/1200px-Cheetah4.jpg"

    generation_id = await start_video_generation(prompt, image_url)
    if not generation_id:
        await message.answer("❌ Ошибка при запуске генерации. Используйте /start чтобы начать заново")
        await state.clear()
        return

    await state.update_data(generation_id=generation_id)
    await message.answer(f"🆔 ID генерации: {generation_id}\n"
                         "⏳ Ожидайте завершения...")

    await state.set_state(VideoStates.waiting_for_generation)

    video_url = await wait_for_video_completion(generation_id)

    if video_url:
        await message.answer_video(video_url, caption="✅ Ваше видео готово!")
    else:
        await message.answer("❌ Не удалось сгенерировать видео. Используйте /start чтобы начать заново")

    await state.clear()


@router.message(VideoStates.waiting_for_photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    await message.answer("✅ Фото получено! Теперь введите описание видео:")
    await state.update_data(photo_file_id=file_id)
    await state.set_state(VideoStates.waiting_for_prompt)


