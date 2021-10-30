import asyncio
#from data.config import QIWI_ST, QIWI_PHONE

import aiohttp
from SimpleQIWI import *

from datetime import datetime, timezone, timedelta

token = '31093f320368ad6d9ada8b2ac9e2b7e9' #QIWI_ST
phone = '+79189656523' #QIWI_PHONE


class Qiwi():
    def __init__(self, token, phone):
        self.token = token
        self.phone = phone

    async def create_bill(self, amount, comment):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            data = {"amountInteger": amount, "currency": 643, "extra['comment']": comment, "extra['account']": self.phone, "extra['accountType']": 'nickname'}
            async with session.get(f"https://qiwi.com/99999", params=data) as response:
                print(response.real_url)




qiwi = Qiwi(token, phone)

loop = asyncio.get_event_loop()
loop.run_until_complete(qiwi.create_bill('10', '213939'))