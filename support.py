import telebot
import time
from dotenv import load_dotenv
import os
from threading import Lock

# Загружаем переменные окружения из файла .env
load_dotenv('config.env')

# Токен Telegram бота и ID чата поддержки
TELEGRAM_SUPPORT_TOKEN = os.getenv('TELEGRAM_SUPPORT_TOKEN')
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')

# Создаем объект бота
bot = telebot.TeleBot(TELEGRAM_SUPPORT_TOKEN)

# Храним время последней заявки и блокировку для многозадачности
last_request_time = 0
request_lock = Lock()

# Словарь для хранения связи между пользователями и их заявками
user_requests = {}

# Функция для обработки всех входящих сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global last_request_time
    
    current_time = time.time()

    # Проверяем, прошло ли хотя бы 45 секунд с последней заявки
    with request_lock:
        if current_time - last_request_time >= 45:
            last_request_time = current_time

            # Сохраняем ID пользователя и текст заявки для дальнейшего использования
            user_requests[message.from_user.id] = {
                'user_id': message.from_user.id,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'message': message.text,
                'time': current_time
            }

            # Пересылаем заявку в чат поддержки
            bot.send_message(SUPPORT_CHAT_ID, f"Новая заявка от {message.from_user.first_name} ({message.from_user.id}):\n\n{message.text}")

            # Подтверждаем пользователю, что его заявка отправлена в поддержку
            bot.send_message(message.chat.id, "Ваша заявка отправлена в чат поддержки. Ответим вам как можно скорее.")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, подождите минимум 45 секунд перед отправкой следующей заявки.")

# Функция для обработки сообщений от поддержки
@bot.message_handler(func=lambda message: message.chat.id == SUPPORT_CHAT_ID)
def handle_support_reply(message):
    # Проверяем, содержит ли сообщение информацию о пользователе
    if message.text.startswith("Ответ пользователю:"):
        user_id = extract_user_id_from_message(message.text)

        if user_id in user_requests:
            user_message = user_requests[user_id]
            
            # Отправляем ответ пользователю
            bot.send_message(user_message['user_id'], f"Ответ от поддержки: {message.text[18:]}")
            bot.send_message(SUPPORT_CHAT_ID, f"Ответ отправлен пользователю {user_message['first_name']} ({user_message['user_id']})")
        else:
            bot.send_message(SUPPORT_CHAT_ID, "Не удалось найти пользователя для ответа.")
    else:
        bot.send_message(SUPPORT_CHAT_ID, "Пожалуйста, укажите формат ответа с информацией о пользователе.")

# Функция для извлечения user_id из сообщения поддержки
def extract_user_id_from_message(text):
    """
    Извлекаем user_id из текста ответа, который должен быть в формате:
    'Ответ пользователю: [user_id] текст ответа'
    """
    try:
        user_id_str = text.split("Ответ пользователю: ")[1].split()[0]
        return int(user_id_str)
    except (IndexError, ValueError):
        return None

# Запуск бота
bot.polling(none_stop=True)
