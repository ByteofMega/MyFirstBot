import json
import time
import uuid
import os

import requests

import base64

from aiogram.types import Message, FSInputFile
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from core.utils.states_kandinsky import StepsKandinsky


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


# if __name__ == '__main__':
#     api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'B265F11D1235186546FCE169AEE801BA', '6CD101A9583864F6643065EA74FF3D4E')
#     model_id = api.get_model()
#     uuid = api.generate("Sun in sky", model_id)
#     images = api.check_generation(uuid)
#     print(images)


async def get_kandinsky(message: Message, state: FSMContext):
    await message.answer('Введите свой промпт.')
    await state.set_state(StepsKandinsky.GET_PROMPT)


async def print_image_kandinsky(message: Message, bot: Bot, state: FSMContext, directory='images_ai'):
    if message.text == '/cancel':
        await message.answer('Выход из режима генерации картинок ИИ (Kandinsky).')
        await state.clear()
    else:
        prompt = message.text
        await message.answer('Ваше изображение генерируется')
        print(prompt)
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'YOUR_API_KEY',
                            'YOUR_SECRET_KEY')
        model_id = api.get_model()
        uuid_g = api.generate(f"{prompt}", model_id)
        images = api.check_generation(uuid_g)
        image_base64 = images[0]
        image_data = base64.b64decode(image_base64)

        image_name = str(uuid.uuid4()) + '.png'
        file_path = os.path.join(directory, image_name)

        with open(file_path, 'wb') as file:
            file.write(image_data)
        finished_image = FSInputFile(file_path)
        await bot.send_photo(message.chat.id, finished_image)
        await message.answer('Вы можете написать еще запрос или прекратить режим генерации картинок командой /cancel')
        os.remove(file_path)

# import logging
# import aiohttp
# from aiogram import Bot, Dispatcher, F
# from aiogram.types import Message, InputFile
# from aiogram.client.session.aiohttp import AiohttpSession
# import base64
# from io import BytesIO
#
# API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Замените на токен вашего бота
# KANDINSKY_API_URL = 'https://api.kandinsky.com/generate'
# KANDINSKY_API_KEY = 'YOUR_KANDINSKY_API_KEY'  # Если API требует ключ
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
#
# async def start_handler(message: Message):
#     await message.answer("Привет! Отправь мне текст, и я попытаюсь сгенерировать изображение через Kandinsky 3.0.")
#
# async def text_handler(message: Message):
#     async with aiohttp.ClientSession() as session:
#         # Отправка запроса к API Kandinsky 3.0
#         async with session.post(KANDINSKY_API_URL, json={'text': message.text, 'api_key': KANDINSKY_API_KEY}) as resp:
#             if resp.status == 200:
#                 data = await resp.read()
#                 image_data = base64.b64decode(data)  # Декодирование строки base64 в байты
#                 image = BytesIO(image_data)  # Создание объекта BytesIO из байтов
#                 image.name = 'image.png'
#
#                 await message.answer_photo(photo=InputFile(image))
#             else:
#                 logging.error(f"Failed to generate image: {resp.status}")
#                 await message.answer("Не удалось сгенерировать изображение через Kandinsky 3.0.")
#
# async def main():
#     bot = Bot(token=API_TOKEN, session=AiohttpSession())
#     dp = Dispatcher()
#
#     dp.message.filter(F.text.startswith('/start')).register(start_handler)
#     dp.message.filter(~F.text.startswith('/start')).register(text_handler)
#
#     await dp.start_polling(bot, allowed_updates=[Message])
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
