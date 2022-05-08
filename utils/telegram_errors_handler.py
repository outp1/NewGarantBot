import json
import logging
import requests

class TelegramHandler(logging.Handler):

    def __init__(self, bot_token: str, admin_id: str, bot_name: str):
        self.bot_name = bot_name
        self.admin_id = admin_id
        self.url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        super().__init__(level=logging.ERROR)
        print('GOOD')


    def emit(self, record: logging.LogRecord):
        logEntry = self.format(record)
        text = f"""
К тебе взывает робот <b>{self.bot_name}</b>:
<code>{logEntry}</code>
"""
        data = {
            'text': text,
            'chat_id': self.admin_id,
            'parse_mode': 'HTML'
        }
        print('\n\nPOSTING ERROR TO BOT \n')
        response = requests.post(self.url, data=data)
        print(response.json(), '\n\n')

