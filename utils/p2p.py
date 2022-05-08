#   Copyright (c) 2021. Tocenomiczs

from datetime import datetime, timezone, timedelta
from typing import Union
import json

import requests


class QiwiP2P:
    _secret_key: str

    def __init__(self, secret_key: str):
        self._secret_key = secret_key

    def generate_bill(self, bill_sum: Union[float, int], bill_id: Union[str, int]):
        headers = {
            "Authorization": f"Bearer {self._secret_key}",
            "Accept": "application/json"
        }

        data = {
            "amount": {
                "value": bill_sum,
                "currency": "RUB"
            },
            "expirationDateTime": (datetime.now(timezone(timedelta(hours=3))) + timedelta(days=31)).strftime(
                "%Y-%m-%dT%H:%M:%S+03:00"
            ),
            "comment": f"Оплата счёта #{bill_id}"
        }
        response = requests.put(f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}", headers=headers,
                                json=data)
        response = json.loads(response.text)
        if response.get("errorCode") is not None:
            print(response)
            return False
        return response['payUrl']

    def is_bill_payed(self, bill_id: Union[str, int]):
        headers = {
            "Authorization": f"Bearer {self._secret_key}",
            "Accept": "application/json"
        }
        response = requests.get(f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}", headers=headers).json()
        if response.get("errorCode") is not None:
            print(response)
            return False
        if response['status']['value'] != "PAID":
            return False
        return True

    def reject_bill(self, bill_id: Union[str, int]):
        headers = {
            "Authorization": f"Bearer {self._secret_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        requests.post(f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}/reject", headers=headers)