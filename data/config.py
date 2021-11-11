from environs import Env
from utils.db_api.req_database import ReqDatabase

req_con = ReqDatabase('utils/db_api/db.db')

env = Env()
env.read_env()

BOT_TOKEN =  '1909718638:AAHowBBJ9vp5fSYekAU00RVFTKGobu2HWGk'
ADMINS = [1344493803, 1850543498]
IP = '' #НЕ обязательно

LOG_CHAT = [-1001599363239] #чат для логов
SERVICES_CHAT = [-1001545297908] #чат услуг
WITHDRAW_CHAT = [-684222153] #чат выводов(приватный)


MODERATORS = [1344493803, 1850543498] #пока неважно

def qiwi():
    qiwi = req_con.qiwi()
    if qiwi:
        QIWI_ST = qiwi[1] #токен киви
        QIWI_PHONE = qiwi[3] #киви телефон
        NICK = qiwi[4] #киви никнейм
    else:
        QIWI_ST = '31093f320368ad6d9ada8b2ac9e2b7e9'  # токен киви
        QIWI_PHONE = '+79189656523'  # киви телефон
        NICK = 'OUTPL'  # киви никнейм
    return QIWI_ST, QIWI_PHONE, NICK

def banker():
    banker = req_con.banker()
    print(banker)
    if banker:
        API_ID = banker[1]#апи приложения телеграм
        API_HASH = banker[2] #апи хеш приложения телеграмм
        NUMBER_T = banker[3] #номер телефона тг
        if banker[4] == '':
            PASSWORD = None #пароль тг
        PASSWORD = banker[4]
    else:
        API_ID = '8953973'
        API_HASH = 'acd4fe4c101f5f9f4313621606ad5c50'
        NUMBER_T = '79189656523'
        PASSWORD = ''
    return API_ID, API_HASH, NUMBER_T, PASSWORD



