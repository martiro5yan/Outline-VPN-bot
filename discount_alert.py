import requests
import text
import sqlite3 as sl
import database
from dotenv import load_dotenv
import os

def list_users():
    con = sl.connect(database.db_path)
    cur = con.cursor()

    cur.execute("SELECT tg_user_id FROM trial_users WHERE is_paid = 0")
    result = cur.fetchall()
    tg_users_id = [user[0] for user in result]
    con.close()
    return tg_users_id  # Возвращаем список пользователей

# Загружаем переменные окружения из файла .env
load_dotenv('config.env')
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Сообщение, которое нужно отправить
message = text.discount_month

# URL для отправки сообщений через Telegram Bot API
url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

# Получаем список пользователей
tg_users_id = list_users()

# Отправляем сообщение каждому пользователю из списка
for user_id in tg_users_id:
    payload = {
        'chat_id': user_id,
        'text': message
    }

    # Отправляем запрос к Telegram API
    response = requests.post(url, data=payload)

    # Проверка успешности запроса
    if response.status_code == 200:
        print(f"Сообщение отправлено пользователю {user_id}!")
    else:
        print(f"Ошибка при отправке сообщения пользователю {user_id}: {response.status_code}, {response.text}")
