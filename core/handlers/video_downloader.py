import yt_dlp
import os

from aiogram.types import Message, FSInputFile
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from core.utils.states_yt_download import StepsYtDownloader


# URL видео на YouTube
# video_url = 'https://youtu.be/tzk5Cb8IpsY?si=qYy9tzy_yGEYuKW3'
#
# # Путь для сохранения видео
# output_path = '/videos'
#
# download_youtube_video(video_url, output_path)


def download_youtube_video(url, output_path='.'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
    return file_path


async def get_url(message: Message, state: FSMContext):
    await message.answer('Введите ссылку видео')
    await state.set_state(StepsYtDownloader.GET_URL)


async def download_and_send_video(message: Message, bot: Bot, state: FSMContext):
    if message.text == '/cancel':
        await message.answer('Выход из режима скачивания видео')
        await state.clear()
    else:
        url = message.text
        await message.reply("Видео загружается, подождите немного...")

        try:
            video_path = download_youtube_video(url, output_path='/videos')
            video_file = FSInputFile(video_path)
            await message.answer_video(video_file)

            # Удаление видео после отправки
            os.remove(video_path)
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")
            os.remove('/videos')
