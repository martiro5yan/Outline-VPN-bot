import telebot
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv('config.env')

TOKEN = os.getenv('TELEGRAM_SUPPORT_TOCEN')
SUPPORT_CHAT_ID = int(os.getenv('SUPPORT_CHAT_ID'))  # Убедитесь, что это int
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения заявок (message_id в чате поддержки -> user_id)
pending_requests = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Опишите вашу проблему, и мы постараемся помочь.")

@bot.message_handler(func=lambda message: message.chat.id != SUPPORT_CHAT_ID)
def forward_to_support(message):
    """Пересылает сообщение пользователя в поддержку."""
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет username"
    full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()

    # Формируем текст заявки
    edited_text = (
        f"📩 Новая заявка в поддержку\n"
        f"👤 Пользователь: {full_name} ({username})\n"
        f"🆔 ID: {user_id}\n"
        f"💬 Сообщение:\n{message.text}"
    )

    # Отправляем сообщение в поддержку
    sent_message = bot.send_message(SUPPORT_CHAT_ID, edited_text)

    # Сохраняем связь сообщения поддержки с пользователем
    pending_requests[sent_message.message_id] = user_id

    bot.send_message(message.chat.id, "✅ Ваша заявка отправлена в техподдержку.")

@bot.message_handler(func=lambda message: message.chat.id == SUPPORT_CHAT_ID and message.reply_to_message)
def reply_to_user(message):
    """Позволяет техподдержке отвечать пользователю."""
    support_msg_id = message.reply_to_message.message_id  # ID ответа
    user_id = pending_requests.get(support_msg_id)  # Ищем ID пользователя

    if user_id:
        # Отправляем ответ пользователю
        bot.send_message(user_id, f"📩 Ответ от техподдержки:\n{message.text}")
        bot.send_message(message.chat.id, "✅ Ответ отправлен пользователю.")
    else:
        bot.send_message(message.chat.id, "⚠ Ошибка: Исходное сообщение не найдено.")

bot.polling(none_stop=True)
