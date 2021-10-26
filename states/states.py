from aiogram.dispatcher.filters.state import State, StatesGroup

class Deal(StatesGroup):
    search_user = State()