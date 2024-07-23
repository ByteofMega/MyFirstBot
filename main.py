import asyncio
from aiogram import Bot, Dispatcher, F
from core.handlers.basic import get_start, sieg_hail, free_time, show_classic, get_help
from core.utils.commands import set_commands
# from core.settings import settings
from aiogram.filters import Command
from core.handlers import weather
from core.utils.statesweather import StepsWeather
from core.handlers.nasa import get_content_from_nasa
from core.handlers import kandinsky
from core.utils.states_kandinsky import StepsKandinsky
from core.handlers import video_downloader
from core.utils.states_yt_download import StepsYtDownloader

TOKEN = 'YOUR_BOT_TOKEN'
ADMIN_ID = 'YOUR_PROFILE_ID'


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, text='The bot is running!')


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text='The bot is stopped!')


async def start():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command('start'))
    dp.message.register(sieg_hail, Command('hail'))
    dp.message.register(get_help, Command('help'))
    dp.message.register(weather.get_weather, Command('weather'))
    dp.message.register(weather.print_weather, StepsWeather.GET_CITY)
    dp.message.register(free_time, F.text == 'Что ты делаешь в свободное время?')
    dp.message.register(show_classic, F.text == 'Покажи мне классику')
    dp.message.register(get_content_from_nasa, Command('get_nasa'))
    dp.message.register(kandinsky.get_kandinsky, Command('kandinsky'))
    dp.message.register(kandinsky.print_image_kandinsky, StepsKandinsky.GET_PROMPT)
    dp.message.register(video_downloader.get_url, Command('get_video'))
    dp.message.register(video_downloader.download_and_send_video, StepsYtDownloader.GET_URL)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
