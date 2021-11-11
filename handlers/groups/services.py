from aiogram import types
from loader import dp, bot
from data.config import SERVICES_CHAT
from filters import *
import re

async def find_all_urls(message):
    d = re.findall('<a>', message)

Verif = types.InlineKeyboardMarkup()
Verif.add(types.InlineKeyboardButton(text='✅ Пройти верификацию', url='https://t.me/adm_ebot'))

@dp.message_handler(ServicesChat(), VerifSeller(), state='*')
async def verif_seller(message: types.Message):
    user = await bot.get_chat(message.from_user.id)
    member = await bot.get_chat_member(message.chat.id, user.id)
    if member.status in ['admin', 'creator', 'administrator']:
        return
    if "@gnt_ebot" not in message.text:
        await bot.delete_message(message.chat.id, message.message_id)
        text = f'''
    😢 <b>{user.mention}, вы не указали гарант чата в своём рекламном сообщении!</b>

    <b>Создайте новый пост и добавьте в конце:</b>

    <code>🤝 Гарант - @gnt_ebot</code>
    '''
        await message.answer(text=text)
    else:
        pass
    try: await message.reply(text='⬆ <b>Верифицированный селлер</b> ⬆', reply_markup=Verif)
    except: pass

@dp.message_handler(ServicesChat(), state='*')
async def mentioning(message: types.Message):
    try: user = await bot.get_chat(message.from_user.id)
    except: pass
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status in ['admin', 'creator', 'administrator']:
        return
    for a in message.entities:
        if a.type == "text_link":
            if 'https://t.me/gnt_ebot' not in a.url:
                await bot.delete_message(message.chat.id, message.message_id)
                return await message.answer(f'😢 <b>{user.mention}, вы указали в своём рекламном сообщении сторонний сервис!</b>\n\n' 
                                            f'<b>Вам необходимо пройти верификацию для того, чтобы отправлять подобное</b>', reply_markup=Verif)
        elif a.type == "url":
            links = re.search("(?P<url>https?://[^\s]+)", message.text).group("url").split('\n')
            for link in links:
                try: check = re.search(r'gnt_ebot', link.split('/')[3]).group()
                except: return await bot.delete_message(message.chat.id, message.message_id) and await message.answer(f'😢 <b>{user.mention}, вы указали в своём рекламном сообщении сторонний сервис!</b>\n\n' 
                                            f'<b>Вам необходимо пройти верификацию для того, чтобы отправлять подобное</b>', reply_markup=Verif)
        elif a.type == "mention":
            mentions = re.findall("@\w+", message.text)
            for mention in mentions:
                if mention != '@gnt_ebot':
                    if mention != message.from_user.mention:
                        return await bot.delete_message(message.chat.id, message.message_id) and await message.answer(f'😢 <b>{user.mention}, вы указали в своём рекламном сообщении сторонний сервис!</b>\n\n' 
                                                f'<b>Вам необходимо пройти верификацию для того, чтобы отправлять подобное</b>', reply_markup=Verif)
    if "@gnt_ebot" not in message.text:
        await bot.delete_message(message.chat.id, message.message_id)
        text=f'''
😢 <b>{user.mention}, вы не указали гарант чата в своём рекламном сообщении!</b>

<b>Создайте новый пост и добавьте в конце:</b>

<code>🤝 Гарант - @gnt_ebot</code>
'''
        return await message.answer(text=text)
    else:
        pass



@dp.message_handler()
async def a(message: types.Message):
    print(message.chat.id)


