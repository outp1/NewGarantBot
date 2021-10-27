from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from filters import *
from keyboards import *
from loader import bot, users_con, deal_con
from states import *
from utils.misc import other


async def search_seller(_id):
    seller = users_con.seller(_id)
    return seller


async def set_deal(deal_id, price, description, client, seller):
    deal = deal_con.set_deal(deal_id, price, description, client, seller)
    return deal


async def take_deal(_id):
    deal = deal_con.take_deal(_id)
    return deal


async def deal_status(_id, status=None):
    if status:
        status = deal_con.status(_id, status)
        return
    else:
        deal_con.status(_id)


@dp.message_handler(IsPrivate(), text='Поиск продавца 🔍')
async def search_seller1(message: types.Message):
    await message.answer('🔎<b>  Введите никнейм продавца, с которым хотите совершить сделку</b>',
                         reply_markup=MainKbs.GoMenuMarkup)
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
        return await Deal.search_user.set()

    try:
        seller = await search_seller(mention)
    except:
        seller = None
    if seller:
        pass
    else:
        return await message.answer(
            '❌  Селлер не найден, вероятно он ещё не зарегистрирован в боте, либо сменил никнейм. Во втором случае пусть селлер просто нажмёт на кнопку "/start", и никнейм' +
            ' автоматически обновится!')
    rating = seller[2]
    if rating == 0:
        rating = 'Ещё не совершал ни одной сделки'
    text = f"""
<b>✅    Продавец под никнеймом: </b>{mention}

👉  <b>Рейтинг продавца: </b>{rating}
👉  <b>Статус: </b>{seller[3]}
👉  <b>Дата регистрации: </b>{seller[1]}
👉  <b>Заработано: </b>{seller[4]}

    Выберите действие:
    """
    await state.update_data(seller=seller[0])
    await message.answer(text, reply_markup=MainKbs.SellerMarkup)


# НАЧАЛО СДЕЛКИ
@dp.callback_query_handler(text='MakeDeal', state='*')
async def make_deal(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.answer('Введите сумму сделки: ', reply_markup=MainKbs.InlineGoBack)
    await state.update_data(msg=msg)
    await Deal.price.set()


@dp.message_handler(state=Deal.price)
async def set_deal_desc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg = data['msg']
    await bot.delete_message(message.from_user.id, msg.message_id)
    await bot.delete_message(message.from_user.id, message.message_id)
    if message.text.isdigit():
        msg = await message.answer(
            'Опишите условаия сделки (Описание товара, техническое задание и т.п). Это обязательно и поможет при возникновении спора по сделке',
            reply_markup=MainKbs.InlineGoBack)
        await state.update_data(msg=msg, price=message.text)
        await Deal.description.set()
    else:
        bot.delete_message(message.from_user.id, msg)
        msg = await message.answer('Введите верную сумму сделки, в формате целого числа: ',
                                   reply_markup=MainKbs.InlineGoBack)
        await state.update_data(msg=msg)
        await Deal.price.set()


@dp.message_handler(state=Deal.description)
async def send_deal(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    await bot.delete_message(message.from_user.id, message.message_id)
    user = await bot.get_chat(message.from_user.id)
    seller = await bot.get_chat(data['seller'])
    price = data['price']
    description = message.text
    text = f"""<b>
🤑   Сделка между {seller.mention} и {user.mention}</b>   🤑  

<b>Сумма сделки: </b>{price}
<b>Условия: </b>
{description}

Выберите действие:
"""
    msg = await message.answer(text, reply_markup=MainKbs.SendDealMarkup)
    await state.update_data(msg=msg)


# ОТПРАВИТЬ СДЕЛКУ
@dp.callback_query_handler(text='ConfirmDeal', state='*')
async def send_seller_deal(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.answer('<b>Сделка отправлена продавцу! Вам придёт оповещение когда он её примет ⏱</b>')
    uniq_id = other.rand_id_to_acc()
    print(uniq_id)
    deal = await set_deal(uniq_id, data['price'], data['description'], call.from_user.id, data['seller'])
    print(deal)
    client = await bot.get_chat(deal[3])
    text = f"""
    <b>Сделка под номером <code>{uniq_id}</code> 💰</b>
    
<b>⊳   Покупатель: </b>{client.mention}
<b>⊳   Сумма сделки: </b>{deal[1]}₽
<b>
⊳    Принимаете ли вы сделку?
</b> 
"""
    await bot.send_message(deal[4], text=text, reply_markup=MainKbs.ConfirmSellerMarkup(deal[0]))

# КНОПКИ ПРИНЯТИЯ СДЕЛКИ
@dp.callback_query_handler(MainKbs.confirm_callbackdata.filter(confirm=['True']), state='*')
async def seller_confirm_deal(call: types.CallbackQuery, callback_data: dict):
    deal = await take_deal(callback_data['id'])
    await deal_status(callback_data['id'], '1')
    await call.answer('✅ Сделка принята')
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)
    await bot.send_message(deal[3],
                           text=f'<b>✅  Сделка под номером <code>{callback_data["id"]}</code> принята продавцом!</b>')
@dp.callback_query_handler(MainKbs.confirm_callbackdata.filter(confirm=['False']), state='*')
async def seller_cancel_deal(call: types.CallbackQuery, callback_data: dict):
    deal = await take_deal(callback_data['id'])
    await deal_status(callback_data['id'], '4')
    await call.answer('❌ Вы отказались от сделки')
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)
    await bot.send_message(deal[3],
                           text=f'<b>❌  Продавец отказался от сделки под номером <code>{callback_data["id"]}</code></b>')

# АКТИВНЫЕ СДЕЛКИ ЮЗЕРА
@dp.callback_query_handler(text='MyDeals', state='*')
async def my_deals(call: types.CallbackQuery):
    await call.answer('Загружаем информацию по сделкам...')

# КНОПКИ ОТМЕНЫ
@dp.callback_query_handler(text='CancelDeal', state='*')
async def cancel_deal(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(call.from_user.id, data['msg'].message_id)
@dp.callback_query_handler(text='GoBack', state='*')
async def go_back(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(call.from_user.id, data['msg'].message_id)
    seller = data['seller']
    await state.finish()
    await state.update_data(seller=seller)
