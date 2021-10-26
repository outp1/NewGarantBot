from aiogram import types

MenuMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
SearchSeller = types.KeyboardButton(text='Поиск продавца 🔍')
Profile = types.KeyboardButton(text='Профиль 💼')
Info = types.KeyboardButton(text='Информация 📄')
MenuMarkup.add(Profile, Info).add(SearchSeller)

GoMenuMarkup = types.InlineKeyboardMarkup()
GoMenu = types.InlineKeyboardButton(text='Назад 🔙', callback_data='GoMenu')
GoMenuMarkup.add(GoMenu)

GoMenuDMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
GoDMenu = types.KeyboardButton(text='Назад 🔙')
GoMenuDMarkup.add(GoDMenu)

ProfileMarkup = types.InlineKeyboardMarkup()
ReplenishBalance = types.InlineKeyboardButton(text='Пополнить баланс 💵', callback_data='ReplenishBalance')
Withdraw = types.InlineKeyboardButton(text='Вывести средства ⤴', callback_data='Withdraw')
ProfileMarkup.add(ReplenishBalance).add(Withdraw).add(GoMenu)

