from aiogram import types
from aiogram.utils.callback_data import CallbackData

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
MyDeals = types.InlineKeyboardButton(text='Активные сделки ⏱', callback_data='MyDeals')
ReplenishBalance = types.InlineKeyboardButton(text='Пополнить баланс 💵', callback_data='ReplenishBalance')
Withdraw = types.InlineKeyboardButton(text='Вывести средства ⤴', callback_data='Withdraw')
ProfileMarkup.add(MyDeals).add(ReplenishBalance, Withdraw).add(GoMenu)

SellerMarkup = types.InlineKeyboardMarkup()
MakeDeal = types.InlineKeyboardButton(text='Отправить сделку 🚀', callback_data='MakeDeal')
Reviews = types.InlineKeyboardButton(text='Отзывы 🏅', callback_data='Reviews')
SellerMarkup.add(MakeDeal).add(Reviews)

InlineGoBack = types.InlineKeyboardMarkup()
GoBack = types.InlineKeyboardButton(text='Назад 🔙', callback_data='GoBack')
InlineGoBack.add(GoBack)

SendDealMarkup = types.InlineKeyboardMarkup()
ConfirmDeal = types.InlineKeyboardButton(text='Подтвердить сделку ✅', callback_data='ConfirmDeal')
CancelDeal = types.InlineKeyboardButton(text='Отмена 🙅', callback_data='CancelDeal')
SendDealMarkup.add(ConfirmDeal).add(CancelDeal)

confirm_callbackdata = CallbackData('confirm_callbackdata', 'id', 'confirm')
def ConfirmSellerMarkup(_id):
    ConfirmSellerMarkup = types.InlineKeyboardMarkup()
    confirm = types.InlineKeyboardButton(text='Принять ✅', callback_data=confirm_callbackdata.new(_id, True))
    cancel = types.InlineKeyboardButton(text='Отказаться ❌', callback_data=confirm_callbackdata.new(_id, False))
    ConfirmSellerMarkup.add(confirm).add(cancel)
    return ConfirmSellerMarkup


