from aiogram.dispatcher.filters.state import State, StatesGroup

class Deal(StatesGroup):
    search_user = State()
    price = State()
    description = State()