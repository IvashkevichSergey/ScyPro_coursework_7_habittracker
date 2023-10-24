import requests

from config.settings import TELEGRAM_API_TOKEN

# CHAT_ID = '2131932811'


def get_chat_id():
    """Сервисная функция для получения chat_id у Телеграм бота"""
    url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/getUpdates'
    res = requests.get(url)
    try:
        chat_id = res.json()['result'][0]['message']['chat']['id']
        return chat_id
    except Exception as e:
        print(e)
        print('Something went wrong...')
