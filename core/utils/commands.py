from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Getting started'
        ),
        BotCommand(
            command='weather',
            description='Показывает погоду в указанном городе. Для получения данных напишите город'
        ),
        BotCommand(
            command='get_nasa',
            description='Отправляет фото дня или видео дня от NASA'
        ),
        # BotCommand(
        #     command='sd_image_ai',
        #     description='Создает изображение по вашему запросу через ИИ (Stable Diffusion) (только на английском)'
        # ),
        BotCommand(
            command='kandinsky',
            description='Создает изображение по вашему запросу через ИИ (Kandinsky 3.0)'
        ),
        BotCommand(
            command='get_video',
            description='Скачивает видео по ссылке (только YouTube, не дольше 20 мин)'
        ),
        BotCommand(
            command='help',
            description='Список команд'
        )

    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
