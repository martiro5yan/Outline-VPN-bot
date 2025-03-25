import requests
import sys
import outline

from dotenv import load_dotenv
import os



load_dotenv('config.env')
BOT_TOCEN = os.getenv('TELEGRAM_TOCEN')

print('удаление ключа')

user_id = sys.argv[1]

message = "Ваш пробный период завершен, ключ удален. Однако у вас есть 50% скидка на первый месяц использования\n /start для обновления цены"

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
    
else:
    print(f"Ошибка: {response.status_code}, {response.text}")