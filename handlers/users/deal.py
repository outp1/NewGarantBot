from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from filters import *
from keyboards import *
from loader import bot, users_con, deal_con, feed_con
from states import *
from utils.misc import other

from data.config import LOG_CHAT, SERVICES_CHAT, MODERATORS

async def mailing_dispute(text, deal, user, seller):
    for chat in MODERATORS:
        await bot.send_message(chat, text=text, reply_markup=MainKbs.DisputeMarkup(deal, user, seller))

async def mailing_services(text):
    for chat in SERVICES_CHAT:
        await bot.send_message(chat, text=text)

async def mailing_logchat(text):
    for chat in LOG_CHAT:
        await bot.send_message(chat, text=text)

async def _user(_id, mention=None):
    user = users_con.user(_id, mention)
    return user

async def search_seller(_id):
    seller = users_con.seller(_id)
    return seller

async def set_deal(deal_id, price, description, client, seller):
    deal = deal_con.set_deal(deal_id, price, description, client, seller)
    return deal


async def take_deal(_id):
    deal = deal_con.take_deal(_id)
    return deal

async def active_deals(_id):
    return deal_con.active_deals(_id)

async def delete_deal(_id):
    deal_con.delete_deal(_id)


async def deal_status(_id, status=None):
    if status:
        status = deal_con.status(_id, status)
        return
    else:
        deal_con.status(_id)

async def update_balance(_id, amount, earned=False, minus=False):
    users_con.update_balance(_id, amount, earned, minus)

async def set_feed(deal, seller, rate):
    feed_con.add_feed(deal, seller, rate)
    rating = feed_con.calc_rating(seller)
    users_con.update_rating(seller, rating)



@dp.message_handler(IsPrivate(), text='🔍 Поиск продавца', state='*')
async def search_seller1(message: types.Message, state: FSMContext):
    await state.finish()
    msg = await message.answer('🔍 <b>Введите никнейм продавца, с которым хотите начать сделку</b>',
                         reply_markup=MainKbs.GoMenuMarkup)
    await state.update_data(msg=msg)
    await Deal.search_user.set()


@dp.message_handler(state=Deal.search_user)
async def take_seller(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
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
<b>🔍 Продавец: </b>{mention}

📊 <b>Рейтинг продавца:</b> {rating}
✅ <b>Статус: </b>{seller[3]}
📆 <b>Дата регистрации: </b>{seller[1]}
💳 <b>Сумма сделок: </b>{seller[4]}
    """
    await state.update_data(seller=seller[0])
    await message.answer(text, reply_markup=MainKbs.SellerMarkup)


# НАЧАЛО СДЕЛКИ
@dp.callback_query_handler(text='MakeDeal', state='*')
async def make_deal(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.answer("🚀 <b>Введите сумму сделки:</b>", reply_markup=MainKbs.InlineGoBack)
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
            '🚀 <b>Опишите условия сделки</b>(Описание товара, техническое задание). <b>Это обязательно</b> и поможет при возникновении спора по сделке.',
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
    price = data['price']
    user = await bot.get_chat(message.from_user.id)
    seller = await bot.get_chat(data['seller'])
    description = message.text
    text = f"""<b>
🤑   Сделка между {seller.mention} и {user.mention}</b>   🤑  

<b>Сумма сделки: </b>{price}
<b>Условия: </b>
{description}

<b>Выберите действие:</b>
"""
    msg = await message.answer(text, reply_markup=MainKbs.SendDealMarkup)
    await state.update_data(msg=msg)



# ОТПРАВИТЬ СДЕЛКУ
@dp.callback_query_handler(text='ConfirmDeal', state='*')
async def send_seller_deal(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    uniq_id = other.rand_id_to_acc()
    data = await state.get_data()
    balance = await _user(call.from_user.id)
    deal = await set_deal(uniq_id, data['price'], data['description'], call.from_user.id, data['seller'])
    if int(balance[5]) >= int(deal[1]):
        try: await update_balance(call.from_user.id, int(deal[1]), minus=True)
        except: return await call.answer('❌ Ошибка ❌')
        await call.message.answer('🚀 <b>Запрос о начале сделки отправлен продавцу</b>')
        client = await bot.get_chat(deal[3])
        text = f"""
🚀 <b>Проверьте условия и подтвердите начало сделки</b>

💸 <b>Сумма сделки:</b> {deal[1]}RUB
📝 <b>Условия:</b>
{deal[2]}
"""
        await bot.send_message(deal[4], text=text, reply_markup=MainKbs.ConfirmSellerMarkup(deal[0]))
        await state.finish()
    else:
        await delete_deal(deal[0])
        await call.message.answer("<b>❌  На балансе недостаточно средств, пополните баланс через профиль  ❌</b>")

# КНОПКИ ПРИНЯТИЯ СДЕЛКИ
@dp.callback_query_handler(MainKbs.confirm_callbackdata.filter(confirm=['True']), state='*')
async def seller_confirm_deal(call: types.CallbackQuery, callback_data: dict):
    deal = await take_deal(callback_data['id'])
    await deal_status(callback_data['id'], '1')
    await call.answer('✅ Сделка принята')
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)
    await bot.send_message(deal[3],
                           text=f'✅ <b>Сделка под номером</b> <code>{deal[0]}</code> <b>принята продавцом!</b>')
    user = await _user(deal[3])
    seller = await _user(deal[4])
    text=f""" 
<b>♻️ Между {user[6]} и {seller[6]} началась сделка !️ ♻️
Айди сделки: <code>{deal[0]}</code>
Сумма сделки: <code>{deal[1]}</code>₽
</b>
"""
    await mailing_services(text)

@dp.callback_query_handler(MainKbs.confirm_callbackdata.filter(confirm=['False']), state='*')
async def seller_cancel_deal(call: types.CallbackQuery, callback_data: dict):
    deal = await take_deal(callback_data['id'])
    await deal_status(callback_data['id'], '4')
    await update_balance(deal[3], deal[1])
    await call.answer('❌ Вы отказались от сделки')
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)
    await bot.send_message(deal[3],
                           text=f'<b>❌  Продавец отказался от сделки под номером <code>{callback_data["id"]}</code></b>')

# АКТИВНЫЕ СДЕЛКИ ЮЗЕРА
@dp.message_handler(text='🤝 Сделки', state='*')
async def my_deals(message: types.Message):
    await message.answer('Загружаем информацию по сделкам...')
    deals = await active_deals(message.from_user.id)
    for a in deals[0]:
        seller = await bot.get_chat(a[4])
        user = await bot.get_chat(a[3])
        text = f"""
🚀 <b>Проверьте условия и подтвердите начало сделки</b>

💸 <b>Сумма сделки:</b> {a[1]}RUB
📝 <b>Условия:</b>
{a[2]}
</b> 
"""
        await message.answer(text=text, reply_markup=MainKbs.ConfirmSellerMarkup(a[0]))
    deals = await active_deals(message.from_user.id)
    for a in deals[1]:
        seller = await bot.get_chat(a[4])
        user = await bot.get_chat(a[3])
        text = f"""<b>
🤑   Сделка между {seller.mention} и {user.mention}</b>   🤑  

<b>Сумма сделки: </b>{a[1]}
<b>Условия: </b>
{a[2]}

<b>Ожидайте пока продавец примет или отменит вашу сделку</b>
"""
        await message.answer(text)
    deals = await active_deals(message.from_user.id)
    for a in deals[2]:
        seller = await bot.get_chat(a[4])
        user = await bot.get_chat(a[3])
        text = f"""
🤝 <b>Сделка {a[0]}</b>

👨‍💼 <b>Продавец: {seller.mention}</b>
💁‍♂ <b>Покупатель: {user.mention}</b>

💸 <b>Сумма сделки:</b> {a[1]}
📝 <b>Условия:</b>
{a[2]}
"""
        await message.answer(text=text, reply_markup=MainKbs.BuyDealsMarkup(a[0]))
    deals = await active_deals(message.from_user.id)
    for a in deals[3]:
        seller = await bot.get_chat(a[4])
        user = await bot.get_chat(a[3])
        text = f"""
<b>Сделка под номером <code>{a[0]}</code> 💰</b>
    
<b>⊳   Покупатель: </b>{user.mention}
<b>⊳   Сумма сделки: </b>{a[1]}₽
<b>⊳   Условия сделки:</b>
{a[2]}
<b>
⊳    Выберите действие:
</b> 
"""
        await message.answer(text=text, reply_markup=MainKbs.SellDealsMarkup(a[0]))

# ОТПРАВИТЬ, ВЕРНУТЬ ДЕНЬГИ ИЛИ ОТКРЫТЬ СПОР ПО СДЕЛКЕ
@dp.callback_query_handler(MainKbs.buydeals_callback_data.filter(send_money='True'), state='*')
async def buydeals_sendmoney(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    msg = await call.message.answer('<b>✌️Оцените качество товара написав цифру от 1 до 10: </b>')
    await Feed.rate.set()
    await state.update_data(deal=callback_data['_id'], send=callback_data['send_money'], msg=msg)
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)

@dp.message_handler(state=Feed.rate)
async def set_rate(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try: await bot.delete_message(message.from_user.id, data['msg'].message_id)
    except: pass
    try: rate = int(message.text)
    except:
        await message.answer('<b>✌️Оцените качество товара написав цифру от 1 до 10: </b>')
        return await Feed.rate.set()
    if (rate > 10) and (rate < 1):
        await message.answer('<b>✌️Оцените качество товара написав цифру от 1 до 10: </b>')
        return await Feed.rate.set()
    await state.update_data(rate=rate)
    text = '<b>Подтвердите действие, и деньги будут отправлены, а сделка закрыта</b>'
    await message.answer(text, reply_markup=MainKbs.ConfirmBuydeals)


@dp.callback_query_handler(MainKbs.selldeals_callback_data.filter(dispute='False'), state='*')
async def selldeals_returnmoney(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = '<b>Подтвердите действие, и деньги будут возвращены, а сделка закрыта</b>'
    await call.message.answer(text, reply_markup=MainKbs.ConfirmReturnMoney)
    await state.update_data(deal=callback_data['_id'], dispute=callback_data['dispute'])
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)

@dp.callback_query_handler(MainKbs.selldeals_callback_data.filter(dispute='True'), state='*')
async def selldeals_dispute(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text= '<b>Подтвердите действие и сделка будет переведена в режим арбитража</b>'
    await call.message.answer(text, reply_markup=MainKbs.ConfirmDispute)
    await state.update_data(deal=callback_data['_id'], send='seller')
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)

@dp.callback_query_handler(MainKbs.buydeals_callback_data.filter(send_money='False'), state='*')
async def selldeals_dispute(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text= '<b>Подтвердите действие и сделка будет переведена в режим арбитража</b>'
    await call.message.answer(text, reply_markup=MainKbs.ConfirmDispute)
    await state.update_data(deal=callback_data['_id'], send='user')
    with suppress(MessageNotModified):
        await bot.edit_message_text('<b>' + call.message.text + '</b>', call.from_user.id, call.message.message_id)

# КНОПКИ ПОДТВЕРЖДЕНИЯ ДЕЙСТВИЙ
@dp.callback_query_handler(text='ConfirmDispute', state='*')
async def ConfirmDispute(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deal = await take_deal(data['deal'])
    if data['send'] == 'user':
        user = await _user(deal[3])
        seller = await _user(deal[4])
        await call.message.answer('<b>Сделка переведена в режим арбитража, ожидайте ответа администратора...</b>')
        await bot.send_message(deal[4],
                               f'<b>❕  Покупатель сделки под номером <code>{deal[0]}</code> только что перевёл сделку в режим арбитража, ожидайте сообщения администратора!  ❕</b>')
        await deal_status(deal[0], 3)
        text1 = f"""<b>
🛑  Спор между покупателем {user[6]} и селлером {seller[6]}  🛑 

Сумма сделки: {deal[1]}₽
Условия сделки: 
{deal[2]}
</b>
            """
        await mailing_dispute(text1, deal[0], user[0], seller[0])
    else:
        user = await _user(deal[3])
        seller = await _user(deal[4])
        await call.message.answer('<b>Сделка переведена в режим арбитража, ожидайте ответа администратора...</b>')
        await bot.send_message(deal[3],
                               '<b>❕  Продавец только что перевёл сделку в режим арбитража, ожидайте сообщения администратора!  ❕</b>')
        await deal_status(deal[0], 3)
        text1 = f"""<b>
🛑  Спор между покупателем {user[6]} и селлером {seller[6]}  🛑 

Сумма сделки: {deal[1]}₽
Условия сделки: 
{deal[2]}
</b>
"""
        await mailing_dispute(text1, deal[0], user[0], seller[0])




@dp.callback_query_handler(text='ConfirmBuydeals', state='*')
async def confirm_send_money(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deal = await take_deal(data['deal'])
    if deal[5] == 1:
        if data['send'] == 'True':
            await set_feed(deal[0], deal[4], data['rate'])
            await update_balance(deal[4], deal[1], earned=True)
            await deal_status(deal[0], 2)
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await call.answer('✅ Деньги отправлены')
            user = await _user(deal[3])
            seller = await _user(deal[4])
            text =f"""<b>
🥳       Сделка под номером <code>{deal[0]}</code> завершена!     🥳
🥳       На ваш баланс поступило <code>{deal[1]}</code>₽             🥳     
            
            </b>
            """
            await bot.send_message(text=text, chat_id=deal[4])
            text1 = f""" 
            <b>♻ {user[6]} и {seller[6]} только что завершили сделку! ♻️
Айди сделки: <code>{deal[0]}</code>
Сумма сделки: <code>{deal[1]}</code>₽
            </b>
            """
            await mailing_services(text1)
            await call.message.answer('<b>Сделка завершена, деньги отправлены продавцу!</b>')
            #await call.message.answer('Вы можете оставить отзыв продавцу!', reply_markup=MainKbs.FeedBackMarkup(deal[4]))

    else:
        return await call.message.answer('<b>Деньги за данную сделку уже отправлены ✌</b>')


@dp.callback_query_handler(text='ConfirmReturnMoney', state='*')
async def confirm_return_money(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deal = await take_deal(data['deal'])
    if deal[5] == 1:
        if data['dispute'] == 'False':
            await update_balance(deal[3], deal[1])
            await deal_status(deal[0], 2)
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await call.answer('✅ Деньги отправлены')
            text = f"""<b>
♻️Деньги за сделку под номером <code>{deal[0]}</code> возвращены продавцом!
♻️На ваш баланс поступило <code>{deal[1]}</code>₽

                        </b>
                        """
            await bot.send_message(text=text, chat_id=deal[3])
    else:
        return await call.message.answer('<b>Деньги за данную сделку уже отправлены ✌</b>')


# КНОПКИ СПОРА МОДЕРАТОРА
@dp.callback_query_handler(MainKbs.dispute_callbackdata.filter(), state='*')
async def dispute_buttons(call: types.CallbackQuery, callback_data: dict):
    await call.answer('✅ Деньги отправлены')
    await bot.edit_message_text(chat_id=call.from_user.id, text=call.message.text, message_id=call.message.message_id)
    deal = await take_deal(callback_data['deal'])
    earned = False
    if str(callback_data['won']) == str(deal[4]):
        earned = True
    await update_balance(callback_data['won'], deal[1], earned=earned)
    await bot.send_message(callback_data['won'], text='<b>🥳  Вы выиграли спор, деньги зачислены на ваш баланс!  🥳</b>')
    await deal_status(deal[0], 4)

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

@dp.callback_query_handler(text='Reviews', state='*')
async def Reviews(call: types.CallbackQuery, state: FSMContext):
    await call.answer('⏱ Отзывы пока не добавлены')

@dp.callback_query_handler(text='Referal', state='*')
async def Reviews(call: types.CallbackQuery, state: FSMContext):
    await call.answer('❕ Реферальная система пока не работает')




