from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = [1344493803, 1850543498]
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

LOG_CHAT = [-1001576386008, 1850543498]
SERVICES_CHAT = [-1001576386008]
WITHDRAW_CHAT = [-1001576386008]


MODERATORS = ['1344493803']

QIWI_ST = '31093f320368ad6d9ada8b2ac9e2b7e9'
QIWI_PHONE = '+79189656523'
NICK = 'OUTPL'

API_ID = '8953973'
API_HASH = 'acd4fe4c101f5f9f4313621606ad5c50'
NUMBER_T = '+79189656523'
