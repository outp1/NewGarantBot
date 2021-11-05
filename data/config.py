from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = '1909718638:AAHowBBJ9vp5fSYekAU00RVFTKGobu2HWGk'
ADMINS = [1344493803, 1850543498]
IP = '' #НЕ обязательно

LOG_CHAT = [] #чат для логов
SERVICES_CHAT = [] #чат услуг
WITHDRAW_CHAT = [] #чат выводов(приватный)


MODERATORS = [] #пока неважно

QIWI_ST = '' #токен киви
QIWI_PHONE = '' #киви телефон
NICK = '' #киви никнейм

API_ID = '' #апи приложения телеграм
API_HASH = '' #апи хеш приложения телеграмм
NUMBER_T = '' #номер телефона тг
PASSWORD = '' #пароль тг
