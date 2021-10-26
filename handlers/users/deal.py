from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards import *
from aiogram.dispatcher.storage import FSMContext
from loader import dp, bot, users_con
from filters import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from states import *

@dp.message_handler(IsPrivate(), text='Поиск продавца 🔍')
async def search_seller(message: types.Message):
    await message.answer('🔎<b>  Введите никнейм продавца, с которым хотите совершить сделку: </b>', reply_markup=MainKbs.GoMenuMarkup)
    await Deal.search_user.set()

@dp.message_handler(state=Deal.search_user)
async def take_seller(message: types.Message, state: FSMContext):
    mention = message.text
    if '@' in mention:
        if len(mention) <= 30:
            pass
        else:
            await message.answer('Никнейм слишком длинный, повторите ввод:', reply_markup=MainKbs.GoMenuMarkup)
            await Deal.search_user.set()

    else:
        await message.answer('Введите правильный никнейм в формате: @ + nickname', reply_markup=MainKbs.GoMenuMarkup)
        await Deal.search_user.set()



