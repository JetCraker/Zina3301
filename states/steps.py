from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminSteps(StatesGroup):
    name = State()
    quantity = State()
    price = State()
    photo = State()


class ToDelete(StatesGroup):
    find_to_delete = State()
    check = State()
    to_delete = State()
