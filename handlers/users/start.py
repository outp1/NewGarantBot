from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards import *
from aiogram.dispatcher.storage import FSMContext
from loader import dp, bot, users_con
from filters import *
from aiogram.dispatcher.filters.state import StatesGroup, State

async def _user(_id):
    user = users_con.user(_id)
    return user

#СТАРТ
@dp.message_handler(text='Назад 🔙')
@dp.message_handler(CommandStart(), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(f"Меню", reply_markup=MainKbs.MenuMarkup)
    await _user(message.from_user.id)

@dp.callback_query_handler(text='GoMenu', state='*')
async def bot_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Меню", reply_markup=MainKbs.MenuMarkup)
    await _user(call.from_user.id)

#ПРОФИЛЬ
@dp.message_handler(IsPrivate(), text='Профиль 💼')
async def profile(message: types.Message):
    user = await _user(message.from_user.id)
    chat = await bot.get_chat(message.from_user.id)
    rating = user[2]
    verif = user[3]
    if verif == 'Неверефицированный':
        verif = verif + ' <a href="https://google.com">(Верификация)</a>'
    if rating == 0:
        rating = 'Вы ещё не совершали ни одной сделки'
    text = f"""
🔑  <b>Вы перешли в профиль, {chat.first_name}  </b>🔑

💰  <b>Баланс: </b>{user[5] + '₽'}

🖱  <b>Ваш рейтинг продавца: </b>{rating}
🖱  <b>Статус: </b>{verif}
🖱  <b>Дата регистрации: </b>{user[1]}
🖱  <b>Заработано: </b>{user[4]}

"""
    await message.answer(text, reply_markup=MainKbs.ProfileMarkup)

#ИНФОРМАЦИЯ
@dp.message_handler(IsPrivate(), text='Информация 📄')
async def send_info(message: types.Message):
    text = f"""
    <b>
   ❓ Как пользоваться ботом ❓
    </b>
    ........
    <b>
  🐦  О проекте  🐦
    </b>
    ........
    """
    await message.answer(text, reply_markup=MainKbs.GoMenuDMarkup)







