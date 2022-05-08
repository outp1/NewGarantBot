from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards import *
from aiogram.dispatcher.storage import FSMContext
from loader import dp, bot, users_con, ref_con, req_con
from filters import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from data.config import ADMINS
from states.states import Admin
from .deal import _user
from utils.misc import other

async def switch_banker(token, api_hash, login, _pass):
    req_con.switch_banker(token, api_hash, login, _pass)

async def switch_qiwi(token, phone, nick):
    req_con.update_qiwi(token, phone, nick)

async def get_refs(_id):
    return users_con.check_refs(_id)

async def generate_link(text):
    ref_con.generate_link(text)

async def take_link_stats(text):
    return ref_con.take_link(str(text))


@dp.callback_query_handler(text='downloads_logs', state='*', is_admin=True)
async def downloads_logs(call: types.CallbackQuery):
    file = other.take_last_logfile()
    files = {'logfile': file}
    file = open(file, 'rb')
    await call.message.answer_document(document=file)

@dp.message_handler(IsPrivate(), commands='ebot', state='*', is_admin=True)
async def adm_panel(message: types.Message):
    await message.answer('<b>Админ панель:</b>', reply_markup=AdmKbs.MainMarkup)

@dp.callback_query_handler(text='back_adm', is_admin=True, state='*')
async def adm_panel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('<b>Админ панель:</b>', reply_markup=AdmKbs.MainMarkup)

@dp.callback_query_handler(text='requisites', state='*')
async def requisites_s(call: types.CallbackQuery):
    await call.message.answer('Выберите какую платежку обновить:', reply_markup=AdmKbs.Requisites)

@dp.callback_query_handler(text='switch_banker')
async def switch_banker(call: types.CallbackQuery):
    await call.message.answer('Введите новый апи токен: ', reply_markup=AdmKbs.BackMarkup)
    await Admin.api_id_banker.set()

@dp.message_handler(state=Admin.api_id_banker)
async def banker1(message: types.Message, state: FSMContext):
    await message.answer('Введите новый апи хеш токен: ', reply_markup=AdmKbs.BackMarkup)
    await state.update_data(api_id=message.text)
    await Admin.api_hash.set()

@dp.message_handler(state=Admin.api_hash)
async def banker2(message: types.Message, state: FSMContext):
    await message.answer('Введите номер телефона от телеграмм аккаунта: ', reply_markup=AdmKbs.BackMarkup)
    await state.update_data(api_hash=message.text)
    await Admin.number_banker.set()

@dp.message_handler(state=Admin.number_banker)
async def banker3(message: types.Message, state: FSMContext):
    await message.answer('Введите пароль от телеграмм аккаунта: ', reply_markup=AdmKbs.BackMarkup)
    await state.update_data(number_banker=message.text)
    await Admin.pass_banker.set()

@dp.message_handler(state=Admin.pass_banker)
async def banker4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    passw = message.text
    await switch_banker(data['api_id'], data['api_hash'], data['number_banker'], passw)
    await message.answer('Новый банкир привязан')



@dp.callback_query_handler(text='switch_qiwi')
async def switch_qiwi(call: types.CallbackQuery):
    await call.message.answer('Введите новый секретный токен: ', reply_markup=AdmKbs.BackMarkup)
    await Admin.qiwi_st.set()

@dp.message_handler(state=Admin.qiwi_st)
async def qiwi1(message: types.Message, state: FSMContext):
    await message.answer('Введите номер телефона киви кошелька: ', reply_markup=AdmKbs.BackMarkup)
    await state.update_data(token=message.text)
    await Admin.qiwi_phone.set()

@dp.message_handler(state=Admin.qiwi_phone)
async def qiwi2(message: types.Message, state: FSMContext):
    await message.answer('Введите никнейм киви кошелька: ', reply_markup=AdmKbs.BackMarkup)
    await state.update_data(phone=message.text)
    await Admin.qiwi_nick.set()

@dp.message_handler(state=Admin.qiwi_nick)
async def qiwi3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    nick = message.text
    await switch_qiwi(data['token'], data['phone'], nick)
    await message.answer('Новый киви привязан')

@dp.callback_query_handler(text='manage_user', state='*')
async def ref_stats(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text='Введите айди пользователя: ', reply_markup=AdmKbs.BackMarkup)
    await Admin.id_refs.set()

@dp.message_handler(state=Admin.id_refs)
async def check_refs(message: types.Message, state: FSMContext):
    user = await _user(int(message.text))
    text = f'''
Айди пользователя: {str(user[0])}
Количество приведенных человек: {user[7]}
Бланас: {user[5]}
Сумма сделок: {user[4]}
Дата регистрации: {user[1]}
Рейтинг: {user[2]}
Статус: {user[3]}

    '''
    await message.answer(text=text, reply_markup=AdmKbs.UserMarkup(user[0]))

@dp.message_handler(commands='verif', state='*')
async def take_verif(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer('Айди юзера:')
        await Admin.id_verif.set()

@dp.message_handler(state=Admin.id_verif)
async def set_verif(message: types.Message, state: FSMContext):
    users_con.take_verif(message.text)
    await state.finish()

@dp.callback_query_handler(text='referals')
async def referals(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text='Выберите действие: ', reply_markup=AdmKbs.ReferalsMarkup)

@dp.callback_query_handler(text='generate_ref', state='*')
async def generate_ref(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите заголовок ссылки: ')
    await Admin.ref_name.set()

@dp.message_handler(state=Admin.ref_name)
async def ref_name(message: types.Message):
    await generate_link(message.text)
    text=f'''
✅ <b>Ссылка сгенерирована: </b>
https://t.me/gnt_ebot?start={message.text}
    '''
    await message.answer(text=text)

@dp.callback_query_handler(text='check_ref', state='*')
async def check_ref(call: types.CallbackQuery):
    await call.message.answer('Введите заголовок ссылки:', reply_markup=AdmKbs.BackMarkup)
    await Admin.ref_name_check.set()

@dp.message_handler(state=Admin.ref_name_check)
async def ref_stats(message: types.Message):
    a = await take_link_stats(message.text)
    if a:
        text=f'''<b>
Ссылка: 
https://t.me/gnt_ebot?start={message.text}
Количество переходов в бота: <code>{a}</code>
</b>
'''
        await message.answer(text=text)
    else:
        await message.answer('Ссылка не найдена, введите другой заголовок: ', reply_markup=AdmKbs.BackMarkup)
        await Admin.ref_name_check.set()

@dp.callback_query_handler(AdmKbs.user_markup_callbackdata.filter(wtodo='balance'), state='*')
async def update_user_balance(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer('Введите какой баланс сделать пользователю: ', reply_markup=AdmKbs.BackMarkup)
    await state.update_data(id=callback_data['id'])
    await Admin.update_balance_adm.set()

@dp.message_handler(state=Admin.update_balance_adm)
async def update_balance(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try: users_con.set_balance(data['id'], int(message.text))
    except: return await message.answer('Ошибка')




