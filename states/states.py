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

    id_verif = State()
    id_refs = State()

    api_id_banker = State()
    api_hash = State()
    number_banker = State()
    pass_banker = State()

    qiwi_st = State()
    qiwi_phone = State()
    qiwi_nick = State()

    ref_name = State()
    ref_name_check = State()

    update_balance_adm = State()