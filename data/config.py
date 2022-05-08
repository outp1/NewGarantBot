from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
ADMIN = env.str("ADMIN")
BOT_NAME = env.str("BOT_NAME")

LOG_CHAT = env.str("LOG_CHAT") #чат для логов
SERVICES_CHAT = env.list("SERVICES_CHAT") #чат услуг
WITHDRAW_CHAT = env.str("WITHDRAW_CHAT") #чат выводов(приватный)


MODERATORS = env.list("MODERATORS")

FOLDER_LOGS = env.str("FOLDER_LOGS")
LOGGING_CONFIG_FILE = env.str("LOGGING_CONFIG_FILE")

POSTGRESQLITE = {
    'user': env.str("POSTGRES_USER"),
    'password': env.str("POSTGRES_PASSWORD"),
    'host': env.str("POSTGRES_HOST"),
    'port': env.str("POSTGRES_PORT"),
    'database': env.str("POSTGRES_DB")}

def qiwi():
    QIWI_ST = env.str("DEFAULT_QIWI_ST")
    QIWI_PHONE = env.str("DEFAULT_QIWI_NUMBER")
    NICK = env.str("DEFAULT_QIWI_NICK")
    return QIWI_ST, QIWI_PHONE, NICK

def banker():
    API_ID = env.str("DEFAULT_API_ID")
    API_HASH = env.str("DEFAULT_API_HASH")
    NUMBER_T = env.str("DEFAULT_NUMBER_T")
    PASSWORD = env.str("DEFAULT_PASSWORD")
    return API_ID, API_HASH, NUMBER_T, PASSWORD



