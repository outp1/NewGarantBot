import logging

from aiogram import executor
import loader
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands



async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)



    # logging.getLogger('aiogram').removeHandler(logging.handlers.RotatingFileHandler)
    # logging.getLogger('telethon').removeHandler(logging.handlers.RotatingFileHandler)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)



