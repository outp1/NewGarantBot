import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards import *
from aiogram.dispatcher.storage import FSMContext
from loader import dp, bot, users_con
from filters import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from data.config import ADMINS, SERVICES_CHAT
from states.states import Admin

async def _user(_id, mention=None, ref=None):
    user = users_con.user(_id, mention, ref)
    return user


#СТАРТ
@dp.message_handler(text='⬅', state='*')
@dp.message_handler(CommandStart(), IsPrivate(), state='*')
async def bot_start(message: types.Message):
    chat = await bot.get_chat(message.from_user.id)
    mention = chat.mention
    text = '🔝 <b>Главное меню</b>'
    for i in SERVICES_CHAT:
        print('CHAT:', i)
        chat_check = await bot.get_chat(i)
        status = await bot.get_chat_member(i, message.from_user.id)
        if status.status in ['left', 'kicked']:
            link = await chat_check.get_url()
            print(link)
            return await message.answer(f'❕ <b>Чтобы пользоваться гарант ботом вступите в чат услуг проекта:</b>', reply_markup=MainKbs.LinkServices(link))
    if '@' in mention:
        if message.text[7:]:
            await _user(message.from_user.id, mention, message.text[7:])
        else:
            await _user(message.from_user.id, mention)
    else:
        if message.text[7:]:
            await _user(message.from_user.id, mention, message.text[7:])
        else:
            await _user(message.from_user.id)
        text = text + '\n\n‼ <b>Для корректного использования бота, пожалуйста, установите себе никнейм в настройках и снова напишите /start</b>'
    await message.answer(text=text, reply_markup=MainKbs.MenuMarkup)

@dp.message_handler(IsNotSub(), state='*')
async def msg(m: types.Message, state: FSMContext):
    try: await state.finish()
    except: pass
    chatss = []
    uid = m.from_user.id
    for i in SERVICES_CHAT:
        chat = await bot.get_chat(i)
        status = await bot.get_chat_member(i, uid)
        if status.status in ['left', 'kicked']:
            link = await chat.get_url()
            chatss.append(f'<a href="{link}">{chat.title}</a>')
    if len(chatss) >= 1:
        return await m.answer(f'❕ <b>Чтобы пользоваться гарант ботом вступите в чат услуг проекта:</b>',
                                    reply_markup=MainKbs.LinkServices(link))

@dp.callback_query_handler(text='GoMenu', state='*')
async def bot_start(call: types.CallbackQuery, state: FSMContext):
    try: await bot.delete_message(call.from_user.id, call.message.message_id)
    except: pass
    await state.finish()
    await call.message.answer(text='🔝 <b>Главное меню</b>', reply_markup=MainKbs.MenuMarkup)
    chat = await bot.get_chat(call.from_user.id)
    mention = chat.mention
    if '@' in mention:
        await _user(call.from_user.id, mention=mention)
    else:
        await _user(call.from_user.id)

@dp.chat_member_handler(is_group_join=True, state='*')
async def new_user_channel(update: types.ChatMemberUpdated, state: FSMContext):
    try: await bot.get_chat(update.new_chat_member.user.id)
    except:
        try: await state.finish()
        except: pass
        return
    chatss = []
    a = await state.get_data()
    try:
        ref_id = a['ref_id']
    except:
        ref_id = 0
    uid = update.new_chat_member.user.id
    for i in SERVICES_CHAT:
        status = await bot.get_chat_member(i, uid)
        if status.status in ['left', 'kicked']:
            chatss.append(1)
        if update.new_chat_member.status == 'member':
            chatss == 0
    if len(chatss) == 0:
        user = await _user(str(uid))
        await bot.send_message(uid, text=
                                     f'<b>Вы вступили в чат услуг. Приступайте к работе!</b>')
        await bot.send_photo(uid, photo='AgACAgIAAxkBAAIS1WGFSiEISawI2JOKlAE2MnQtwvx6AAJLuDEbrQQpSDzi9IGsnYwrAQADAgADcwADIgQ', caption='🔝 <b>Главное меню</b>',
                             reply_markup=MainKbs.MenuMarkup)


import requests
from utils.misc import other
#ПРОФИЛЬ
@dp.message_handler(IsPrivate(), text='💁‍♂ Профиль', state='*')
async def profile(message: types.Message, state: FSMContext):
    await state.finish()
    user = await _user(message.from_user.id)
    chat = await bot.get_chat(message.from_user.id)
    rating = user[2]
    verif = user[3]
    if rating == 0:
        rating = 'Вы ещё не совершали ни одной сделки'
    text = f"""
🆔 <b>Ваш id: </b>{message.from_user.id}

💰 <b>Баланс: </b>{str(user[5])}RUB
💳 <b>Сумма сделок: </b>{user[4]} RUB

✅ <b>Статус: </b>{verif}
📊 <b>Рейтинг: </b>{rating}
"""
    await message.answer(text, reply_markup=(await MainKbs.CheckVerif(message.from_user.id)))

#ПРОФИЛЬ
@dp.callback_query_handler(text='GoBackProfile', state='*')
async def profile(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = await _user(call.from_user.id)
    chat = await bot.get_chat(call.from_user.id)
    rating = user[2]
    verif = user[3]
    if verif == 'Неверифицрованный':
        verif = verif + ' <a href="https://google.com">(Верификация)</a>'
    if rating == 0:
        rating = 'Вы ещё не совершали ни одной сделки'
    text = f"""
🆔 <b>Ваш id: </b>{call.from_user.id}

💰 <b>Баланс: </b>{str(user[5])}RUB
💳 <b>Сумма сделок: </b>{user[4]} RUB

✅ <b>Статус: </b>{verif}
📊 <b>Рейтинг: </b>{rating}
    """
    await call.message.answer(text, reply_markup=MainKbs.ProfileMarkup)

#ИНФОРМАЦИЯ
@dp.message_handler(IsPrivate(), text='ℹ Инфо', state='*')
async def send_info(message: types.Message, state: FSMContext):
    await state.finish()
    text = f"""
С помощью данного сервиса, вы сможете приобрести аккаунты, прокси, документы и многое другое!

🤐 <b>Полностью анонимно</b>
Мы не храним логи и прочую информацию.
💸 <b>Низкая комиссия</b>
В разы ниже, чем у конкурентов.
⏰ <b>Очень удобно</b>
Автоматическое открытие и закрытие сделок, моментальный вывод средств.
🎟 <b>Постоянные скидки</b>
Скидки, розыгрыши, раздачи каждую неделю.
☎ <b>Отзывчивая поддержка</b>
Быстрое решение споров, возврат средств.
🤖 <b>Ничего лишнего</b>
В боте нет ничего, что может помешать комфортному использованию.
    """
    await message.answer(text, reply_markup=MainKbs.InfoMarkup)







