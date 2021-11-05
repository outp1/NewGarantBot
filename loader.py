from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import *

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

users_con = UsersDatabase('utils/db_api/db.db')
deal_con = DealsDatabase('utils/db_api/db.db')
feed_con = FeedDatabase('utils/db_api/db.db')
w_con = WithdrawDatabase('utils/db_api/db.db')

