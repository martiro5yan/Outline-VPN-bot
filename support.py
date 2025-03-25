import telebot
import time
from dotenv import load_dotenv
import os
from threading import Lock

# Загружаем переменные окружения из файла .env
load_dotenv('config.env')

# Токен Telegram бота и ID чата поддержки
TOKEN = os.getenv('TELEGRAM_SUPPORT_TOCEN')
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения заявок (message_id в чате поддержки -> user_id)
pending_requests = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Опишите вашу проблему, и мы постараемся помочь.")

@bot.message_handler(func=lambda message: message.chat.id != SUPPORT_CHAT_ID)
def forward_to_support(message):
    """Редактирует сообщение и отправляет его в чат поддержки."""
    first_name = message.from_user.first_name or "Неизвестно"
    last_name = message.from_user.last_name or ""
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет username"

    # Формируем отредактированное сообщение
    edited_text = (f"📩 Новая заявка в поддержку\n👤 Пользователь: {first_name} {last_name} ({username})\n🆔 ID: `{user_id}`\n💬 Сообщение:\n_{message.text}_"
    )

    # Отправляем сообщение в поддержку и сохраняем его ID
    sent_message = bot.send_message(SUPPORT_CHAT_ID, edited_text)
    pending_requests[sent_message.message_id] = message.chat.id

    bot.send_message(message.chat.id, "✅ Ваша заявка отправлена в техподдержку.")

@bot.message_handler(func=lambda message: message.chat.id == SUPPORT_CHAT_ID and message.reply_to_message)
def reply_to_user(message):
    """Позволяет техподдержке отвечать пользователю."""
    support_msg_id = message.reply_to_message.message_id  # ID сообщения, на которое ответила поддержка
    user_id = pending_requests.get(support_msg_id)  # Получаем ID пользователя

    if user_id:
        bot.send_message(user_id, f"📩 *Ответ от техподдержки:*\n{message.text}", parse_mode="Markdown")
        bot.send_message(message.chat.id, "✅ Ответ отправлен пользователю.")
    else:
        bot.send_message(message.chat.id, "⚠ Ошибка: Не найдено исходное сообщение.")

bot.polling(none_stop=True)