from aiogram import types
from aiogram.utils.callback_data import CallbackData
from loader import users_con

async def _user(_id, mention=None):
    user = users_con.user(_id, mention)
    return user

MenuMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
SearchSeller = types.KeyboardButton(text='🔍 Поиск продавца')
MyDeals = types.KeyboardButton(text='🤝 Сделки')
Profile = types.KeyboardButton(text='💁‍♂ Профиль')
Info = types.KeyboardButton(text='ℹ Инфо')
MenuMarkup.add(SearchSeller).add(MyDeals, Profile).add(Info)

GoMenuMarkup = types.InlineKeyboardMarkup()
GoMenu = types.InlineKeyboardButton(text='⬅', callback_data='GoMenu')
GoMenuMarkup.add(GoMenu)

def LinkServices(link):
    LinkServices = types.InlineKeyboardMarkup()
    LinkServices(types.InlineKeyboardButton(text='👉 Чат', link=link))
    return LinkServices

GoMenuDMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
GoDMenu = types.KeyboardButton(text='⬅')
GoMenuDMarkup.add(GoDMenu)


async def CheckVerif(_id):
    ProfileMarkup = types.InlineKeyboardMarkup()
    ReplenishBalance = types.InlineKeyboardButton(text='💸 Пополнить баланс', callback_data='ReplenishBalance')
    Withdraw = types.InlineKeyboardButton(text='📤 Вывести средства', callback_data='Withdraw')
    Promocode = types.InlineKeyboardButton(text='🎟 Активировать промокод', callback_data='Promocode')
    Verif = types.InlineKeyboardButton(text='✅ Верификация', url='https://t.me/fastaccsstore')
    Referal = types.InlineKeyboardButton(text='👥 Реферальная система', callback_data='Referal')
    user = await _user(_id)
    if user[3] == 'Неверифицрованный':
        ProfileMarkup.add(Verif)
    ProfileMarkup.add(Referal).add(ReplenishBalance, Withdraw).add(GoMenu)
    return ProfileMarkup

InfoMarkup = types.InlineKeyboardMarkup()
InfoMarkup.add(types.InlineKeyboardButton(text='💁‍♂ Поддержка', url='https://t.me/hlp_ebot'), types.InlineKeyboardButton(text='👨‍💻 Администратор', url='https://t.me/adm_ebot'))
InfoMarkup.add(types.InlineKeyboardButton(text='💬 Чат', url='https://t.me/inf_ebot'), types.InlineKeyboardButton(text='📣 Реклама', url='https://t.me/adv_ebot'))
InfoMarkup.add(types.InlineKeyboardButton(text='🔥 Другие сервисы', url='https://t.me/inf_ebot'))

GoBackProfile = types.InlineKeyboardMarkup()
GoBackProfile.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='GoBackProfile'))

SellerMarkup = types.InlineKeyboardMarkup()
MakeDeal = types.InlineKeyboardButton(text='🚀 Начать сделку', callback_data='MakeDeal')
Reviews = types.InlineKeyboardButton(text='💫 Отзывы', callback_data='Reviews')
SellerMarkup.add(MakeDeal).add(Reviews)

InlineGoBack = types.InlineKeyboardMarkup()
GoBack = types.InlineKeyboardButton(text='⬅', callback_data='GoBack')
InlineGoBack.add(GoBack)

SendDealMarkup = types.InlineKeyboardMarkup()
ConfirmDeal = types.InlineKeyboardButton(text='🚀 Начать сделку', callback_data='ConfirmDeal')
CancelDeal = types.InlineKeyboardButton(text='🙅 Отмена', callback_data='CancelDeal')
SendDealMarkup.add(ConfirmDeal).add(CancelDeal)

confirm_callbackdata = CallbackData('confirm_callbackdata', 'id', 'confirm')
def ConfirmSellerMarkup(_id):
    ConfirmSellerMarkup = types.InlineKeyboardMarkup()
    confirm = types.InlineKeyboardButton(text='✅ Подтвердить', callback_data=confirm_callbackdata.new(_id, True))
    cancel = types.InlineKeyboardButton(text='❌ Отмена', callback_data=confirm_callbackdata.new(_id, False))
    ConfirmSellerMarkup.add(confirm).add(cancel)
    return ConfirmSellerMarkup

buydeals_callback_data = CallbackData('buydeals_callback_data', '_id', 'send_money')
def BuyDealsMarkup(_id):
    BuyDealsMarkup = types.InlineKeyboardMarkup()
    send_moneys = types.InlineKeyboardButton(text='💸 Отправить средства', callback_data=buydeals_callback_data.new(_id, True))
    open_dispute = types.InlineKeyboardButton(text='👨‍⚖ Открыть спор', callback_data=buydeals_callback_data.new(_id, False))
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

ChooseMethod = types.InlineKeyboardMarkup()
banker = types.InlineKeyboardButton(text='🤖 Banker', callback_data='banker')
card = types.InlineKeyboardButton(text='💳 Карта', callback_data='card')
youmoney = types.InlineKeyboardButton(text='💜 ЮMoney', callback_data='youmoney')
qiwi = types.InlineKeyboardButton(text='🥝 QIWI', callback_data='qiwi')
chatex = types.InlineKeyboardButton(text='💬 Chatex', callback_data='chatex')
ChooseMethod.add(qiwi, youmoney).add(card).add(banker, chatex)

QiwiMethod = types.InlineKeyboardMarkup()
QiwiMethod.add(types.InlineKeyboardButton('✅ Проверить оплату', callback_data='check_qiwi')).add(types.InlineKeyboardButton('❌ Отменить', callback_data='cancel_qiwi'))

QiwiCancel = types.InlineKeyboardMarkup()
QiwiCancel.add(types.InlineKeyboardButton('❌ Отменить', callback_data='cancel_qiwi'))

WithdrawChoose = types.InlineKeyboardMarkup()
WithdrawChoose.add(types.InlineKeyboardButton(text='🥝 QIWI', callback_data='w_qiwi'), types.InlineKeyboardButton(text='🤖 Banker', callback_data='w_banker'))

BackWMarkup = types.InlineKeyboardMarkup()
BackWMarkup.add(types.InlineKeyboardButton(text='Отмена ❌', callback_data='BackWMarkup'))

ConfirmQiwiW = types.InlineKeyboardMarkup()
ConfirmQiwiW.add(types.InlineKeyboardButton(text='✉️Отправить заявку', callback_data='ConfirmQiwiW')).add(types.InlineKeyboardButton('❌ Отменить', callback_data='BackWMarkup'))

w_admin_callbackdata = CallbackData('w_admin_callbackdata', 'w', 'wtodo')
def WAdminMarkup(w):
    WAdminMarkup = types.InlineKeyboardMarkup()
    confirm_w = types.InlineKeyboardButton(text='✅ Подтвердить', callback_data=w_admin_callbackdata.new(w=w, wtodo='confirm'))
    replish_w = types.InlineKeyboardButton(text='♻ Вернуть деньги', callback_data=w_admin_callbackdata.new(w=w, wtodo='replsih'))
    ban_w = types.InlineKeyboardButton(text='❌ Отказать', callback_data=w_admin_callbackdata.new(w=w, wtodo='ban'))
    WAdminMarkup.add(confirm_w).add(replish_w).add(ban_w)
    return WAdminMarkup

banker_admin_callbackdata = CallbackData('banker_admin_callbackdata', 'w', 'wtodo')
def BankerAdminMarkup(w):
    BankerAdminMarkup = types.InlineKeyboardMarkup()
    confirm_banker = types.InlineKeyboardButton(text='✅ Чек отправлен', callback_data=banker_admin_callbackdata.new(w=w, wtodo='confirm'))
    replish = types.InlineKeyboardButton(text='♻ Вернуть деньги', callback_data=banker_admin_callbackdata.new(w=w, wtodo='replish'))
    ban = types.InlineKeyboardButton(text='❌ Отказать', callback_data=banker_admin_callbackdata.new(w=w, wtodo='ban'))
    BankerAdminMarkup.add(confirm_banker).add(replish).add(ban)
    return BankerAdminMarkup

ConfirmBankerW = types.InlineKeyboardMarkup()
ConfirmBankerW.add(types.InlineKeyboardButton(text='✅ Подтвердить', callback_data='ConfirmBankerW')).add(types.InlineKeyboardButton('❌ Отменить', callback_data='BackWMarkup'))

P2PMethod = types.InlineKeyboardMarkup()
P2PMethod.add(types.InlineKeyboardButton('✅ Проверить оплату', callback_data='check_p2p')).add(types.InlineKeyboardButton('❌ Отменить', callback_data='cancel_p2p'))





