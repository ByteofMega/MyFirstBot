import math
import requests
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesweather import StepsWeather

key = 'YOUR_API_KEY'


async def get_weather(message: Message, state: FSMContext):
    await message.answer('Введите название города.')
    await state.set_state(StepsWeather.GET_CITY)


async def print_weather(message: Message, state: FSMContext):
    if message.text == '/cancel':
        await message.answer('Выход из режима получения погоды.')
        await state.clear()
    else:
        try:
            city = message.text
            response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city.lower()}&lang=ru&units=metric&appid={key}')
            data = response.json()
            city = data['name']
            cur_temp = data['main']['temp']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            descriprtion = data['weather'][0]['description']
            await message.reply(f'Погода в городе: {city}\nТемпература: {cur_temp}\n'
                                f'Влажность: {humidity}\nДавление: {math.ceil(pressure)}\nВетер: {wind}\n'
                                f'{str(descriprtion).capitalize()}')
            await message.answer('Чтобы выйти из режима погоды введите /cancel')
        except:
            await message.reply('Проверьте название города!')

