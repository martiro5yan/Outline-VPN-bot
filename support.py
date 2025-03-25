import telebot
import time
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv('config.env')

# Токен Telegram бота и ID чата поддержки
TELEGRAM_SUPPORT_TOKEN = os.getenv('TELEGRAM_SUPPORT_TOCEN')
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')

# Создаем объект бота
bot = telebot.TeleBot(TELEGRAM_SUPPORT_TOKEN)

# Словарь для хранения заявок (message_id чата поддержки -> user_id)
pending_requests = {}

# Словарь для хранения времени последнего сообщения от пользователя
last_request_time = {}

# Минимальный интервал между заявками (в секундах)
REQUEST_DELAY = 45


@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start."""
    bot.send_message(message.chat.id, "Привет! Опишите вашу проблему, и мы постараемся помочь.")


@bot.message_handler(func=lambda message: message.chat.id != SUPPORT_CHAT_ID)
def forward_to_support(message):
    """Перенаправляет сообщения пользователей в чат поддержки с проверкой на спам."""
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка на частоту сообщений
    if user_id in last_request_time and (current_time - last_request_time[user_id]) < REQUEST_DELAY:
        bot.send_message(message.chat.id, f"⏳ Подождите {REQUEST_DELAY} секунд перед следующей заявкой.")
        return

    # Обновляем время последнего сообщения от пользователя
    last_request_time[user_id] = current_time

    # Формируем отредактированное сообщение
    first_name = message.from_user.first_name or "Неизвестно"
    last_name = message.from_user.last_name or "Неизвестно"
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет username"

    edited_text = f"📩 Новая заявка в поддержку\n👤 Пользователь: {first_name} {last_name}\n({username})\n🆔 *ID:* {user_id}\n💬 Сообщение:\n{message.text}"

    try:
        # Отправляем сообщение в чат поддержки
        sent_message = bot.send_message(SUPPORT_CHAT_ID, edited_text)

        # Сохраняем ID отправленного сообщения и соответствующий user_id
        pending_requests[sent_message.message_id] = user_id

        # Подтверждение пользователю, что его заявка отправлена
        bot.send_message(message.chat.id, "✅ Ваша заявка отправлена в техподдержку.")
    except Exception as e:
        # Обработка ошибок при отправке сообщения
        bot.send_message(message.chat.id, "❌ Произошла ошибка при отправке вашей заявки.")
        print(f"Ошибка при отправке сообщения в поддержку: {e}")


@bot.message_handler(func=lambda message: message.chat.id == SUPPORT_CHAT_ID and message.reply_to_message)
def reply_to_user(message):
    """Позволяет техподдержке отвечать пользователю."""
    # Получаем ID сообщения из чата поддержки, на которое был отправлен ответ
    support_msg_id = message.reply_to_message.message_id
    user_id = pending_requests.get(support_msg_id)

    if user_id:
        try:
            # Отправляем ответ пользователю
            bot.send_message(user_id, f"📩 *Ответ от техподдержки:*\n{message.text}", parse_mode="Markdown")

            # Подтверждение техподдержке, что ответ отправлен
            bot.send_message(message.chat.id, "✅ Ответ отправлен пользователю.")
        except Exception as e:
            # Обработка ошибок при отправке ответа
            bot.send_message(message.chat.id, "❌ Ошибка при отправке ответа пользователю.")
            print(f"Ошибка при отправке ответа пользователю: {e}")
    else:
        # Если не найдено исходное сообщение для ответа
        bot.send_message(message.chat.id, "⚠ Ошибка: Не найдено исходное сообщение для ответа.")


# Запускаем бота
bot.polling(none_stop=True)
