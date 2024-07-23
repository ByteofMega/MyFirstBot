from aiogram.fsm.state import StatesGroup, State


class StepsYtDownloader(StatesGroup):
    GET_URL = State()
