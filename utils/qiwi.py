import asyncio
#from data.config import QIWI_ST, QIWI_PHONE
import json
import aiohttp
from glQiwiApi import QiwiWrapper
from datetime import datetime, timezone, timedelta
from data.config import qiwi, banker

token = qiwi()[0]
phone = qiwi()[1]

qiwi1 = QiwiWrapper(token, str(phone))

async def check_bill(amount, comment):
    status = await qiwi1.check_transaction(int(amount), comment=comment)
    return status


class Qiwi():
    def __init__(self, token, phone, nick):
        self.token = token
        self.phone = phone
        self.nick = nick


    async def create_bill(self, amount, comment):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        #https://qiwi.com/payment/form/99999?extra[%27account%27]=79991112233&amountInteger=1&amountFraction=0&extra[%27comment%27]=test123&currency=643
        #https://qiwi.com/99999?extra%5B'account'%5D=%2B79189656523&amountInteger=10&amountFraction=0&extra%5B'comment'%5D=213939&extra%5B'accountType'%5D=nickname&currency=643
        async with aiohttp.ClientSession(headers=headers) as session:
            data = {"extra['account']": self.nick,
                    "amountInteger": amount,
                    'amountFraction': 0,
                    "extra['comment']": comment,
                    "extra['accountType']": 'nickname', "currency": 643}
            async with session.get(f"https://qiwi.com/payment/form/99999", params=data) as response:
                return response.real_url





