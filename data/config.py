from environs import Env
from utils.db_api.req_database import ReqDatabase

req_con = ReqDatabase('utils/db_api/db.db')

env = Env()
env.read_env()

BOT_TOKEN = '1909718638:AAHowBBJ9vp5fSYekAU00RVFTKGobu2HWGk'
ADMINS = [1344493803, 1850543498]
IP = '' #НЕ обязательно

LOG_CHAT = [-1001599363239] #чат для логов
SERVICES_CHAT = [-1001545297908] #чат услуг
WITHDRAW_CHAT = [-684222153] #чат выводов(приватный)


MODERATORS = [] #пока неважно

def qiwi():
    qiwi = req_con.qiwi()
    if qiwi:
        QIWI_ST = qiwi[1] #токен киви
        QIWI_PHONE = qiwi[3] #киви телефон
        NICK = qiwi[4] #киви никнейм
    else:
        QIWI_ST = ''  # токен киви
        QIWI_PHONE = ''  # киви телефон
        NICK = ''  # киви никнейм
    return QIWI_ST, QIWI_PHONE, NICK

def banker():
    banker = req_con.banker()
    if banker:
        API_ID = banker[1]#апи приложения телеграм
        API_HASH = banker[2] #апи хеш приложения телеграмм
        NUMBER_T = banker[3] #номер телефона тг
        PASSWORD = banker[4] #пароль тг
    else:
        API_ID = ''
        API_HASH = ''
        NUMBER_T = ''
        PASSWORD = ''
    return API_ID, API_HASH, NUMBER_T, PASSWORD

