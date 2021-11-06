from aiogram import types

MainMarkup = types.InlineKeyboardMarkup()
MainMarkup.add(types.InlineKeyboardButton(text='Реквизиты', callback_data='requisites'))
MainMarkup.add(types.InlineKeyboardButton(text='Статистика', callback_data='stats'))
MainMarkup.add(types.InlineKeyboardButton(text='Управление пользователем', callback_data='manage_user'))
MainMarkup.add(types.InlineKeyboardButton(text='Рассылка', callback_data='mailing'))
MainMarkup.add(types.InlineKeyboardButton(text='Рефералки', callback_data='referals'))

Requisites = types.InlineKeyboardMarkup()
Requisites.add(types.InlineKeyboardButton(text='Банкир', callback_data='switch_banker'))
Requisites.add(types.InlineKeyboardButton(text='QIWI', callback_data='switch_qiwi'))

BackMarkup = types.InlineKeyboardMarkup()
BackMarkup.add(types.InlineKeyboardButton(text='❌', callback_data='back_adm'))

ReferalsMarkup = types.InlineKeyboardMarkup()
ReferalsMarkup.add(types.InlineKeyboardButton(text='Сгенерировать ссылку', callback_data='generate_ref'))
ReferalsMarkup.add(types.InlineKeyboardButton(text='Проверить ссылку', callback_data='check_ref'))

