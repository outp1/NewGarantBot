from aiogram.dispatcher.filters.state import State, StatesGroup

class Deal(StatesGroup):
    search_user = State()
    price = State()
    description = State()

class Feed(StatesGroup):
    rate = State()

class Payment(StatesGroup):
    amount = State()
    banker = State()
    p2p_amount = State()

class Withdraw(StatesGroup):
    amount = State()
    req = State()
    banker = State()

class Admin(StatesGroup):
    id = State()