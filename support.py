import telebot
import time
from dotenv import load_dotenv
import os

load_dotenv('config.env')

TELEGRAM_SUPPORT_TOCEN = os.getenv('TELEGRAM_SUPPORT_TOCEN')  # Исправлено название переменной
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')  # ID чата поддержки
bot = telebot.TeleBot(TELEGRAM_SUPPORT_TOCEN)

# Словарь для хранения заявок (message_id в чате поддержки -> user_id)
pending_requests = {}
# Словарь для хранения времени последнего сообщения от пользователя
last_request_time = {}
# Минимальный интервал между заявками (в секундах)
REQUEST_DELAY = 45

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Опишите вашу проблему, и мы постараемся помочь.")

@bot.message_handler(func=lambda message: message.chat.id != SUPPORT_CHAT_ID)
def forward_to_support(message):
    """Редактирует сообщение и отправляет его в чат поддержки, проверяя на спам."""
    user_id = message.from_user.id
    current_time = time.time()
    
    # Проверка на частоту сообщений
    if user_id in last_request_time and (current_time - last_request_time[user_id]) < REQUEST_DELAY:
        bot.send_message(message.chat.id, f"⏳ Подождите {REQUEST_DELAY} секунд перед следующей заявкой.")
        return
    
    last_request_time[user_id] = current_time  # Обновляем время последнего сообщения
    
    first_name = message.from_user.first_name or "Неизвестно"
    last_name = message.from_user.last_name or "Неизвестно"
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет username"

    # Формируем отредактированное сообщение
    edited_text = f"📩 Новая заявка в поддержку\n👤 Пользователь: {first_name} {last_name}\n({username})\n🆔 *ID:* {user_id}\n💬 Сообщение:\n{message.text}"

    try:
        # Отправляем сообщение в поддержку и сохраняем ID пользователя
        sent_message = bot.send_message(SUPPORT_CHAT_ID, edited_text)
        pending_requests[sent_message.message_id] = user_id  # Сохраняем user_id, а не message_id

        bot.send_message(message.chat.id, "✅ Ваша заявка отправлена в техподдержку.")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Произошла ошибка при отправке вашей заявки.")
        print(f"Ошибка при отправке сообщения в поддержку: {e}")

@bot.message_handler(func=lambda message: message.chat.id == SUPPORT_CHAT_ID and message.reply_to_message)
def reply_to_user(message):
    """Позволяет техподдержке отвечать пользователю."""
    support_msg_id = message.reply_to_message.message_id  # ID сообщения, на которое ответила поддержка
    user_id = pending_requests.get(support_msg_id)  # Получаем ID пользователя, отправившего заявку

    if user_id:
        try:
            bot.send_message(user_id, f"📩 *Ответ от техподдержки:*\n{message.text}", parse_mode="Markdown")
            bot.send_message(message.chat.id, "✅ Ответ отправлен пользователю.")
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Ошибка при отправке ответа пользователю.")
            print(f"Ошибка при отправке ответа пользователю: {e}")
    else:
        bot.send_message(message.chat.id, "⚠ Ошибка: Не найдено исходное сообщение.")

bot.polling(none_stop=True)