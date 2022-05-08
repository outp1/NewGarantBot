from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import SERVICES_CHAT
from loader import users_con

async def _user(_id):
    return users_con.user(_id)


class ServicesChat(BoundFilter):
    key = 'services_chat'

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        if message.chat.id in SERVICES_CHAT:
            return True

class VerifSeller(BoundFilter):
    key = 'verif_seller'

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        try: user = await _user(message.from_user.id)
        except: return False
        if not user: return False
        if user[3] == 'Верифицированный':
            return True
        else:
            return False
