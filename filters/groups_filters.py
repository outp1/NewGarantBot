from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import SERVICES_CHAT

class ServicesChat(BoundFilter):
    key = 'services_chat'

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        if message.chat.id in SERVICES_CHAT:
            return True