from aiogram import Bot
from aiogram.types import Message


async def get_start(message: Message, bot: Bot):
    await message.answer(f'Привет, {message.from_user.first_name}. Список доступных команд доступно по команде /help.')


async def get_help(message: Message, bot: Bot):
    await message.answer('''Вот список команд:
    /weather - показывает погоду в любом указанном городе
    /get_nasa - отправляет фото дня или видео дня 
    от NASA
    /kandinsky - Создает изображение по вашему 
    запросу
    /get_video - скачивает видео по ссылке (YouTube)
    ''')


async def sieg_hail(message: Message, bot: Bot):
    await message.answer(f'Sieg Hail! {message.from_user.first_name}.')
    await message.answer('✋')


async def free_time(message: Message, bot: Bot):
    await message.answer('Накидываю хайль гитлеров разным людям. Нравится это конечно не всем(')


async def show_classic(message: Message, bot: Bot):
    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEMXwJmewlgnQmSATG37h_Kspim9Z0djgACRg4AAojEQiMsED9EiyT6DzUE')
