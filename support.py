import telebot
import time

TOKEN = "7510972914:AAFZtjTayAhd7UonImhAiGoijfvMoIA9zUE"
SUPPORT_CHAT_ID = -4730642471  # ID чата поддержки

bot = telebot.TeleBot(TOKEN)

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
    edited_text = (
        f"📩 *Новая заявка в поддержку*\n"
        f"👤 *Пользователь:* {first_name} {last_name}\n({username})\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"💬 *Сообщение:*\n_{message.text}_"
    )

    # Отправляем сообщение в поддержку и сохраняем его ID
    sent_message = bot.send_message(SUPPORT_CHAT_ID, edited_text, parse_mode="Markdown")
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
