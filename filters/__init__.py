from aiogram import Dispatcher

from loader import dp
from .is_private import IsPrivate, IsAdmin


if __name__ == "filters":
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin)

