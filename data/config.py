from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

LOG_CHAT = []
SERVICES_CHAT = []

MODERATORS = ['1344493803']

QIWI_ST = '31093f320368ad6d9ada8b2ac9e2b7e9'
QIWI_PHONE = '+79189656523'


