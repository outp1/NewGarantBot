from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards import *
from aiogram.dispatcher.storage import FSMContext
from loader import dp, bot, users_con
from filters import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from data.config import ADMINS
from states.states import Admin

async def _user(_id, mention=None):
    user = users_con.user(_id, mention)
    return user

#СТАРТ
@dp.message_handler(text='⬅', state='*')
@dp.message_handler(CommandStart(), IsPrivate(), state='*')
async def bot_start(message: types.Message):
    chat = await bot.get_chat(message.from_user.id)
    mention = chat.mention
    text = f"""
    Меню
    """
    if '@' in mention:
        await _user(message.from_user.id, mention)
    else:
        await _user(message.from_user.id)
        text = text + '\n\n Для корректного использования бота, пожалуйста, установите себе никнейм в настройках и снова напишите /start'
    await message.answer(text, reply_markup=MainKbs.MenuMarkup)


@dp.callback_query_handler(text='GoMenu', state='*')
async def bot_start(call: types.CallbackQuery, state: FSMContext):
    try: await bot.delete_message(call.from_user.id, call.message.message_id)
    except: pass
    await state.finish()
    await call.message.answer(f"Меню", reply_markup=MainKbs.MenuMarkup)
    chat = await bot.get_chat(call.from_user.id)
    mention = chat.mention
    if '@' in mention:
        await _user(call.from_user.id, mention=mention)
    else:
        await _user(call.from_user.id)

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


@dp.message_handler(commands='verif')
async def take_verif(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer('Айди юзера:')
        await Admin.id.set()

@dp.message_handler(state=Admin.id)
async def set_verif(message: types.Message, state: FSMContext):
    users_con.take_verif(message.text)






