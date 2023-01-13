from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    low = State()
    high = State()

    class Custom(StatesGroup):
        low = State()
        high = State()
