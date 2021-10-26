from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

class IsPrivate(BoundFilter):
    key = 'is_private'

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        if message.from_user.id == message.chat.id:
            return True

