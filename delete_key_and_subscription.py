import requests
import sys
import outline
import database
from dotenv import load_dotenv
import os



load_dotenv('config.env')
BOT_TOCEN = os.getenv('TELEGRAM_TOCEN')

user_id = sys.argv[1]

message = "Ваша подписка окончена, ключ удален!"

url = f'https://api.telegram.org/bot{BOT_TOCEN}/sendMessage'

payload = {
    'chat_id': user_id,
    'text': message
}

response = requests.post(url, data=payload)
    # Проверка успешности запроса
if response.status_code == 200:
    print("Сообщение отправлено!")
    outline.delete_key(user_id)
    database.clear_purchased_key_by_id(user_id)
else:
    print(f"Ошибка: {response.status_code}, {response.text}")