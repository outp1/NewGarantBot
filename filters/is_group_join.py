from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import bot
from data.config import SERVICES_CHAT

class IsGroupJoin(BoundFilter):
    key = "is_group_join"

    def __init__(self, is_group_join: bool):
        self.is_group_join = is_group_join

    async def check(self, update: types.ChatMemberUpdated):
        print(update)
        print(update.new_chat_member.status)
        print(update.old_chat_member.status)
        if update.new_chat_member.status == 'member':
            return True
        if update.new_chat_member.status in ("member", "creator", "left"):
            if str(update.chat.id) in SERVICES_CHAT:
                print('true')
                return True
        elif update.old_chat_member.status in ("member", "administrator", 'admin', "creator", "left"):
            if str(update.chat.id) in SERVICES_CHAT:
                print('true')
                return True

class IsNotSub(BoundFilter):
    async def check(self, m: types.Message):
        uid = m.from_user.id
        chatss = []
        for i in SERVICES_CHAT:
            status = await bot.get_chat_member(i, uid)
            if status.status in ['left', 'kicked']:
                chatss.append(1)
        return len(chatss) >= 1 and m.from_user.id == m.chat.id

