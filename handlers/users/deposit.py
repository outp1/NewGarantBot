from contextlib import suppress

from aiogram import types
from loader import dp, bot
from utils.banker import Banker
from keyboards import MainKbs
from states.states import Payment, Withdraw
from aiogram.dispatcher.storage import FSMContext
from typing import Union
from utils.qiwi import Qiwi, check_bill
from data.config import qiwi, banker, LOG_CHAT, WITHDRAW_CHAT
from loader import deal_con, users_con, w_con
from utils.misc import other
from aiogram.utils.exceptions import MessageNotModified
from utils.p2p import QiwiP2P

data_qiwi = qiwi()
try: data_banker = banker() 
except: data_banker = None #для включения апи клиента, необходимо иметь файл сессии телеграмм аккаунта в корне проекта

if data_banker: 
    try: btc = Banker(data_banker[0], data_banker[1], data_banker[2], data_banker[3])
    except: btc = None #для включения апи клиента, необходимо иметь файл сессии телеграмм аккаунта в корне проекта
qiwi = Qiwi(data_qiwi[0], data_qiwi[1], data_qiwi[2])

async def mailing_logchat(text):
    for chat in LOG_CHAT:
        await bot.send_message(chat, text=text)

async def _user(_id, mention=None):
    user = users_con.user(_id, mention)
    return user

async def update_balance(_id, amount, earned=False, minus=False):
    users_con.update_balance(_id, amount, earned, minus)

async def add_withdraw(_id, user_id, amount, method, req):
    w = w_con.add_withdraw(_id, user_id, amount, method, req)
    return w

async def rand_id():
    return other.rand_id_to_acc()

async def mailing_withdraw(text, reply):
    for chat in WITHDRAW_CHAT:
        await bot.send_message(text=text, chat_id=chat, reply_markup=reply)

async def update_withdraw(_id, status):
    w_con.update_withdraw(_id, status)

async def take_withdraw(_id):
    return w_con.take_withdraw(_id)

@dp.callback_query_handler(text='cancel_qiwi', state='*')
@dp.callback_query_handler(text='ReplenishBalance', state='*')
async def choose_method(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.answer('<b>♻️Выберите способ пополнения: </b>', reply_markup=MainKbs.ChooseMethod)
    await state.update_data(msg=msg)

@dp.callback_query_handler(text='qiwi', state='*')
async def qiwi_amount(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await call.message.answer('<b>Введите сумму пополнения:</b>', reply_markup=MainKbs.QiwiCancel)
    await state.update_data(msg=msg)
    await Payment.amount.set()

@dp.message_handler(state=Payment.amount)
async def qiwi_method(message: types.Message, state: FSMContext):
    amount = message.text
    comment = other.rand_id_to_acc()
    try:
        bill = await qiwi.create_bill(int(amount), comment)
    except (ValueError, TypeError):
        msg = await message.answer('Введите корректную сумму пополнения в виде числа:', reply_markup=MainKbs.QiwiCancel)
        await state.update_data(msg=msg)
        return await Payment.amount.set()
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    href = f'<a href="{bill}">Ссылка на пополнение</a>'
    text = f"""
<b>🥝 Пополнение Qiwi кошелька на сумму <code>{amount}₽</code>
Комментарий обязателен!
</b>
{href}
    """
    await message.answer(text, reply_markup=MainKbs.QiwiMethod)

    await state.update_data(amount=amount, comment=comment)


@dp.callback_query_handler(text='check_qiwi', state='*')
async def check_payment_qiwi(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    status = await check_bill(data['amount'], data['comment'])
    if status:
        await update_balance(call.from_user.id, amount=data['amount'])
        await call.answer('✅ Баланс пополнен')
        await bot.delete_message(call.from_user.id, call.message.message_id)
        text = f"""<b>
♻️Пополнение на {data['amount']}₽  ♻️
Пользователь: {call.from_user.mention}
Способ: Qiwi
</b>
"""
        await mailing_logchat(text=text)
    else:
        await call.answer('Оплата не обнаружена')

@dp.callback_query_handler(text='banker', state='*')
async def banker_cheque(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await call.message.answer('<b>Отправьте чек из @BTC_CHANGE_BOT на желаемую сумму пополнения:</b>', reply_markup=MainKbs.QiwiCancel)
    await state.update_data(msg=msg)
    await Payment.banker.set()

@dp.message_handler(state=Payment.banker)
async def check_cheque(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    cheque = message.text.split('=')[1]
    amount = await btc.check_cheque(cheque)
    """except:
        msg = await message.answer('❌ Ошибка! Отправьте правильный необналиченный чек:')
        await Payment.banker.set()
        await state.update_data(msg=msg)
        """
    if amount:
        await update_balance(message.from_user.id, int(amount))
        await message.answer(f'<b>✅ Баланс пополнен</b>')
        text = f"""<b>
♻️Пополнение на {int(amount)}₽  ♻️
Пользователь: {message.from_user.mention}
Способ: Banker
        </b>
        """
        await mailing_logchat(text=text)
    else:
        msg = await message.answer('❌ Ошибка! Отправьте правильный необналиченный чек:')
        await Payment.banker.set()
        await state.update_data(msg=msg)

# ВЫВОД ДЕНЕГ
@dp.callback_query_handler(text=['Withdraw', 'BackWMarkup'], state='*')
async def ad(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('<b>Выберите способ вывода: </b>', reply_markup=MainKbs.WithdrawChoose)

@dp.callback_query_handler(text='w_qiwi', state='*')
async def w_qiwi(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.answer('<b>Введите сумму вывода: </b>', reply_markup=MainKbs.BackWMarkup)
    await state.update_data(msg=msg)
    await Withdraw.amount.set()

@dp.message_handler(state=Withdraw.amount)
async def qiwi_req(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    user = await _user(message.from_user.id)
    try: amount = int(message.text)
    except:
        msg = await message.answer('<b>Введите корректную сумму вывода: </b>', reply_markup=MainKbs.BackWMarkup)
        await state.update_data(msg=msg)
        return await Withdraw.amount.set()
    if amount < 100:
        msg = await message.answer('<b>Минимальный вывод этим способом составляет 100RUB, введите другую сумму: </b>', reply_markup=MainKbs.BackWMarkup)
        await state.update_data(msg=msg)
        return await Withdraw.amount.set()
    if amount > int(user[5]):
        msg = await message.answer('<b>На балансе недостаточно средств, введите корректную сумму вывода: </b>', reply_markup=MainKbs.BackWMarkup)
        await state.update_data(msg=msg)
        return await Withdraw.amount.set()
    msg = await message.answer('<b>Введите номер телефона киви кошелька: </b>', reply_markup=MainKbs.BackWMarkup)
    await state.update_data(amount=amount, msg=msg)
    await Withdraw.req.set()

@dp.message_handler(state=Withdraw.req)
async def set_w_qiwi(message: types.Message, state: FSMContext):
    req = message.text
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    amount = data['amount']
    text=f"""<b>
♻   Заявка на вывод <code>{amount}₽</code>  
♻   Реквизиты: <code>{req}</code>

Подтвердите отправку: </b>
"""
    await state.update_data(req=req)
    await message.answer(text=text, reply_markup=MainKbs.ConfirmQiwiW)

@dp.callback_query_handler(text='ConfirmQiwiW', state='*')
async def ConfirmQiwiW(call: types.CallbackQuery, state: FSMContext):
    with suppress(MessageNotModified):
        await bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id)
    data = await state.get_data()
    uniq_id = await rand_id()
    w = await add_withdraw(uniq_id, call.from_user.id, data['amount'], 'qiwi', data['req'])
    #except: return await call.message.answer('Ошибка, попробуйте ещё раз')
    user = await bot.get_chat(w[1])
    text=f"""<b>
♻ Заявка на вывод под номером: <code>{w[0]}</code> ♻️
Пользователь: {user.mention}
Сумма вывода: {w[2]}₽
Способ вывода: {w[4]}
Реквизиты: {w[3]}

</b>
"""
    await update_balance(call.from_user.id, amount=w[2], minus=True)
    await mailing_withdraw(text=text, reply=MainKbs.WAdminMarkup(w[0]))
    await call.message.answer(text='<b>⏱ Заявка на вывод успешно сформирована, ожидайте свои средства </b>')

@dp.callback_query_handler(MainKbs.w_admin_callbackdata.filter(wtodo='confirm'))
async def adm_confirm_w(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = call.message.text + '\n\n ДЕНЬГИ ВЫВЕДЕНЫ'
    w = await take_withdraw(callback_data['w'])
    user = await bot.get_chat(w[1])
    with suppress(MessageNotModified):
        await bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id)
    await bot.send_message(w[1], text=f'<b>✅ Заявка на вывод под номером <code>{w[0]}</code> успешно выполнена! </b>')
    await update_withdraw(w[0], 1)
    text = f"""<b> 
♻   {user.mention} только что вывел <code>{w[2]}₽</code> из бота!
</b>
"""
    await mailing_logchat(text=text)

@dp.callback_query_handler(MainKbs.w_admin_callbackdata.filter(wtodo='replsih'))
async def adm_replish_w(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = call.message.text + '\n\n Деньги возвращены'
    w = await take_withdraw(callback_data['w'])
    user = await bot.get_chat(w[1])
    with suppress(MessageNotModified):
        await bot.edit_message_text(text, call.message.sender_chat.id, call.message.message_id)
    await update_balance(w[1], w[2])
    await update_withdraw(w[0], 2)
    await bot.send_message(w[1], text=f'На ваш баланс возвращено {w[2]}₽, вывод отменён администратором')

@dp.callback_query_handler(MainKbs.w_admin_callbackdata.filter(wtodo='ban'))
async def adm_replish_w(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = call.message.text + '\n\n ВЫВОД ЗАБЛОКИРОВАН БЕЗ ВОЗВРАТА СРЕДСТВ'
    w = await take_withdraw(callback_data['w'])
    user = await bot.get_chat(w[1])
    with suppress(MessageNotModified):
        await bot.edit_message_text(text, call.message.sender_chat.id, call.message.message_id)
    await update_withdraw(w[0], 3)

@dp.callback_query_handler(text='w_banker', state='*')
async def w_banker(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.answer('<b>Введите сумму вывода: </b>', reply_markup=MainKbs.BackWMarkup)
    await state.update_data(msg=msg)
    await Withdraw.banker.set()

@dp.message_handler(state=Withdraw.banker)
async def qiwi_req(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    try: amount = int(message.text)
    except:
        msg = await message.answer('<b>Введите корректную сумму вывода: </b>', reply_markup=MainKbs.BackWMarkup)
        await state.update_data(msg=msg)
        return await Withdraw.banker.set()
    if amount < 100:
        msg = await message.answer('<b>Минимальный вывод этим способом составляет 100RUB, введите другую сумму: </b>',
                                   reply_markup=MainKbs.BackWMarkup)
        await state.update_data(msg=msg)
        return await Withdraw.amount.set()
    if amount > int(user[5]):
        msg = await message.answer('<b>На балансе недостаточно средств, введите корректную сумму вывода: </b>',
                                   reply_markup=MainKbs.BackWMarkup)
        await state.update_data(msg=msg)
        return await Withdraw.amount.set()
    await state.update_data(amount=amount)
    await message.answer(f'<b>Подтвердите действие и заявка на вывод {amount}₽ будет создана</b>', reply_markup=MainKbs.ConfirmBankerW)

@dp.callback_query_handler(text='ConfirmBankerW', state='*')
async def ConfirmBankerW(call: types.CallbackQuery, state: FSMContext):
    with suppress(MessageNotModified):
        await bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id)
    data = await state.get_data()
    uniq_id = await rand_id()
    w = await add_withdraw(uniq_id, call.from_user.id, data['amount'], 'banker', call.from_user.id)
    # except: return await call.message.answer('Ошибка, попробуйте ещё раз')
    user = await bot.get_chat(w[1])
    text = f"""<b>
♻ Заявка на вывод под номером: <code>{w[0]}</code> ♻️
Пользователь: {user.mention}
Сумма вывода: {w[2]}₽
Способ вывода: {w[4]}
    </b>
    """
    await update_balance(call.from_user.id, amount=w[2], minus=True)
    await mailing_withdraw(text=text, reply=MainKbs.BankerAdminMarkup(w[0]))
    await call.message.answer(text='<b>⏱ Заявка на вывод успешно сформирована, ожидайте пока вам пришлют чек</b>')


@dp.callback_query_handler(MainKbs.banker_admin_callbackdata.filter(wtodo='confirm'))
async def adm_confirm_w(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = call.message.text + '\n\n ДЕНЬГИ ВЫВЕДЕНЫ'
    w = await take_withdraw(callback_data['w'])
    user = await bot.get_chat(w[1])
    with suppress(MessageNotModified):
        await bot.edit_message_text(call.message.text, call.message.sender_chat.id, call.message.message_id)
    await bot.send_message(w[1], text=f'<b>✅ Заявка на вывод под номером <code>{w[0]}</code> успешно выполнена!</b>')
    await update_withdraw(w[0], 1)
    text = f"""<b> 
♻   {user.mention} только что вывел <code>{w[2]}₽</code> из бота!
</b>
"""
    await mailing_logchat(text=text)

@dp.callback_query_handler(MainKbs.banker_admin_callbackdata.filter(wtodo='replish'))
async def adm_replish_w(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = call.message.text + '\n\n Деньги возвращены'
    w = await take_withdraw(callback_data['w'])
    user = await bot.get_chat(w[1])
    with suppress(MessageNotModified):
        await bot.edit_message_text(text, call.message.sender_chat.id, call.message.message_id)
    await update_balance(w[1], w[2])
    await update_withdraw(w[0], 2)
    await bot.send_message(w[1], text=f'<b>На ваш баланс возвращено {w[2]}₽, вывод отменён администратором</b>')

@dp.callback_query_handler(MainKbs.banker_admin_callbackdata.filter(wtodo='ban'))
async def adm_replish_w(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    text = call.message.text + '\n\n ВЫВОД ЗАБЛОКИРОВАН БЕЗ ВОЗВРАТА СРЕДСТВ'
    w = await take_withdraw(callback_data['w'])
    user = await bot.get_chat(w[1])
    with suppress(MessageNotModified):
        await bot.edit_message_text(text, call.message.sender_chat.id, call.message.message_id)
    await update_withdraw(w[0], 3)

@dp.callback_query_handler(text=['youmoney', 'chatex', 'card'], state='*')
async def no_working(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('❌ <b>Данный способ оплаты, временно, не доступен</b>')


'''
@dp.callback_query_handler(text='card', state='*')
async def p2p_amount(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    msg = await call.message.answer('<b>Введите сумму пополнения:</b>', reply_markup=MainKbs.QiwiCancel)
    await state.update_data(msg=msg)
    await Payment.p2p_amount.set()

@dp.message_handler(state=Payment.p2p_amount)
async def p2p(message: types.Message, state: FSMContext):
    amount = message.text
    comment = other.rand_id_to_acc()

    bill = await qiwi_p2p.generate_bill(int(amount), comment)
    except (ValueError, TypeError):
        msg = await message.answer('Введите корректную сумму пополнения в виде числа:', reply_markup=MainKbs.QiwiCancel)
        await state.update_data(msg=msg)
        return await Payment.p2p_amount.set()
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['msg'].message_id)
    href = f'<a href="{bill}">Ссылка на пополнение</a>'
    text = f"""
<b>🥝 Пополнение кошелька на сумму <code>{amount}₽</code>
Комментарий обязателен!
</b>
{href}
    """
    msg = await message.answer(text, reply_markup=MainKbs.QiwiMethod)

    await state.update_data(amount=amount, comment=comment, msg=msg)

@dp.callback_query_handler(text='check_p2p', state='*')
async def check_payment_p2p(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    status = await qiwi_p2p.is_bill_payed(data['comment'])
    print(status)
    if status:
        await update_balance(call.from_user.id, amount=data['amount'])
        await call.answer('✅ Баланс пополнен')
        await bot.delete_message(call.from_user.id, call.message.message_id)
        text = f"""<b>
♻️Пополнение на {data['amount']}₽  ♻️
Пользователь: {call.from_user.mention}
Способ: CardP2P
</b>
"""
        await mailing_logchat(text=text)
    else:
        await call.answer('Оплата не обнаружена')

@dp.callback_query_handler(text='cancel_p2p', state='*')
async def reject_bill(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    qiwi_p2p.reject_bill(data['comment'])
    await bot.delete_message(call.from_user.id, data['msg'].message_id)
   '''















