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

buydeals_callback_data = CallbackData('buydeals_callback_data', '_id', 'send_money')
def BuyDealsMarkup(_id):
    BuyDealsMarkup = types.InlineKeyboardMarkup()
    send_moneys = types.InlineKeyboardButton(text='Отправить деньги 💵', callback_data=buydeals_callback_data.new(_id, True))
    open_dispute = types.InlineKeyboardButton(text='Открыть спор 👎', callback_data=buydeals_callback_data.new(_id, False))
    BuyDealsMarkup.add(send_moneys).add(open_dispute)
    return BuyDealsMarkup

selldeals_callback_data = CallbackData('selldeals_callback_data', '_id', 'dispute')
def SellDealsMarkup(_id):
    SendDealsMarkup = types.InlineKeyboardMarkup()
    open_dispute = types.InlineKeyboardButton(text='Открыть спор 👎', callback_data=selldeals_callback_data.new(_id, True))
    return_money = types.InlineKeyboardButton(text='Вернуть деньги 💵', callback_data=selldeals_callback_data.new(_id, False))
    SendDealsMarkup.add(open_dispute).add(return_money)
    return SendDealsMarkup

ConfirmBuydeals = types.InlineKeyboardMarkup()
ConfirmBuydeals.add(types.InlineKeyboardButton("✅ Подтверждаю", callback_data='ConfirmBuydeals'))

ConfirmReturnMoney = types.InlineKeyboardMarkup()
ConfirmReturnMoney.add(types.InlineKeyboardButton("✅ Подтверждаю", callback_data='ConfirmReturnMoney'))

ConfirmDispute = types.InlineKeyboardMarkup()
ConfirmDispute.add(types.InlineKeyboardButton("✅ Подтверждаю", callback_data='ConfirmDispute'))

feedback_callbackdata = CallbackData('feedback_callbackdata', 'seller')
def FeedBackMarkup(_id):
    FeedBackMarkup = types.InlineKeyboardMarkup()
    FeedBackMarkup.add(types.InlineKeyboardButton("Оставить отзыв ❤", callback_data=feedback_callbackdata.new(_id)))
    return FeedBackMarkup

dispute_callbackdata = CallbackData('dispute_callbackdata', 'won', 'deal')
def DisputeMarkup (deal, user, seller):
    DisputeMarkup = types.InlineKeyboardMarkup()
    seller_won = types.InlineKeyboardButton('Деньги продавцу 💵', callback_data=dispute_callbackdata.new(won=seller, deal=deal))
    user_won = types.InlineKeyboardButton('Деньги покупателю 💵', callback_data=dispute_callbackdata.new(won=user, deal=deal))
    DisputeMarkup.add(user_won).add(seller_won)
    return DisputeMarkup




