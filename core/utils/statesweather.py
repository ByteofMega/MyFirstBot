from aiogram.fsm.state import StatesGroup, State


class StepsWeather(StatesGroup):
    GET_CITY = State()
    STOP = State()
