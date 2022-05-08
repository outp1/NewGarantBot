from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.config import ADMINS

class IsPrivate(BoundFilter):
    key = 'is_private'

    def __init__(self):
        pass

    async def check(self, message: types.Message):
        if message.from_user.id == message.chat.id:
            return True

class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        if message.from_user.id in ADMINS:
            return True

