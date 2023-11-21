from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminSteps(StatesGroup):
    name = State()
    prise = State()
    photo = State()

