from aiogram.fsm.state import StatesGroup, State


class StepsKandinsky(StatesGroup):
    GET_PROMPT = State()
