import requests
from aiogram import Bot
from aiogram.types import Message
from aiogram.types import FSInputFile

from PIL import Image
import os
import yt_dlp

key = 'YOUR_API_KEY'

url = f'https://api.nasa.gov/planetary/apod?api_key={key}'


def download_video(url, output_path='/videos'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
    return file_path


async def get_content_from_nasa(message: Message, bot: Bot, url=url):  # тестовые функции, нужно скачивать видео с сайта
    await message.answer('Ваш запрос обрабатывается...')  # и отправить пользователю
    # тестовая отправка фото или видео, в дальнейшем нужно скачивать фото/видео и отправлять его пользователю
    try:
        file_path = 'images_ai/picture.png'
        response = requests.get(url)
        data = response.json()
        hd_img_url = data['hdurl']
        hd_img = requests.get(hd_img_url).content
        with open(file_path, 'wb') as image:
            image.write(hd_img)
        img = Image.open(file_path)
        if img.height > 4000 and img.width > 4000:
            height, width = img.height // 3, img.width // 3
            img = img.resize((height, width))
            img.save(file_path)
        finished_image = FSInputFile(file_path)
        await bot.send_photo(message.chat.id, finished_image)
    except Exception as e:
        await message.answer(f'Данные на сегодняшний день не являются фотографией, скачиваю видео. Ошибка {e}')
        response = requests.get(url)
        data = response.json()
        url = data['url']
        video_path = await download_video(url, output_path='/videos')
        video_file = FSInputFile(video_path)
        await message.answer_video(video_file)
        os.remove(video_path)
