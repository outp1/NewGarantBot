from aiogram import types
from loader import dp, bot
from data.config import SERVICES_CHAT
from filters import *


@dp.message_handler(ServicesChat(), state='*')
async def mentioning(message: types.Message):
    user = await bot.get_chat(message.from_user.id)
    member = await bot.get_chat_member(message.chat.id, user.id)
    if member.status in ['admin', 'creator', 'administrator']:
        return
    if "@gnt_ebot" not in message.text:
        await bot.delete_message(message.chat.id, message.message_id)
        text=f'''
😢 <b>{user.mention}, вы не указали гарант чата в своём рекламном сообщении!</b>

<b>Создайте новый пост и добавьте в конце:</b>

<code>🤝 Гарант - @gnt_ebot</code>
'''
        await message.answer(text=text)
    else:
        pass


