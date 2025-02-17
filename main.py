import telebot
from telebot import types
from datetime import datetime

import outline
import text
import invoice_management
import database
import start_at_timer
import txt_manager


admin_id = 395838481

API_TOCEN = '7240622500:AAH12U6R5cksiH0arE_CCvuZRH0PwG4yp1g'
#TECT
#API_TOCEN = '7707295263:AAGW1vLJjvQngYxKOxLUMpH8fpBE2I_8Exc' 

bot = telebot.TeleBot(API_TOCEN)

# Проверка типа входного объекта — является ли он callback'ом
def is_callback(input_data):
    if isinstance(input_data, telebot.types.CallbackQuery):
        return True
    return False

# Получение текущего времени
def current_time():
    return datetime.now()

# Определение идентификатора пользователя
def user_id(data):
    if is_callback(data):
        return data.message.chat.id
    return data.chat.id

# Получение имени пользователя
def username(data):
    return data.from_user.username

# Функция для получения данных пользователя
def user_data(data):
    return user_id(data), data.from_user.username, data.from_user.first_name, data.from_user.last_name

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(admin_id, 'START +1')

    if invoice_management.check_token_validity():
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Нидерланды: 1 месяц 300 ₽', callback_data='300'))
        markup.add(types.InlineKeyboardButton('Инструкция', callback_data='instruction'))
        markup.add(types.InlineKeyboardButton('Техподдержка', url='https://t.me/vpnytSupport_bot'))

        bot.send_message(message.chat.id, text.start_message, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сервис временно не доступен')
        bot.send_message(admin_id, 'Ошибка с токеном Yoomany')
        #Запись пользователей
        txt_manager.save_failed_ids(user_id(message))

# Обработчик команды /manual
@bot.message_handler(commands=['manual'])
def manual_links(user):
    bot.send_message(admin_id, 'MANUAL +1')
    bot.send_message(user.chat.id, text.instruction_text, parse_mode='Markdown')

# Обработчик для кнопки "Инструкция"
@bot.callback_query_handler(func=lambda callback: callback.data == 'instruction')
def send_help(callback):
    bot.send_message(admin_id, 'INSTRU +1')
    bot.send_message(callback.message.chat.id, text.instruction_text, parse_mode='Markdown')

@bot.message_handler(commands=['mykeys'])
def return_user_keys(callback):
    
    bot.send_message(admin_id, 'MYKEYS +1')

    id = user_id(callback)
    
    user = database.get_last_subscription(str(id))
    if user:
        key_name = user[0]
        subscription_end = user[1]
        key = user[2]
    
        response_message = (f"*Окончание подписки:*\n{subscription_end}\n\n"
                    f"*Имя ключа:* ({key_name})\n\n"
                    f"*Ключ:*```{key}```"
        )
        bot.send_message(callback.chat.id, response_message, parse_mode='Markdown')
    else:
        bot.send_message(callback.chat.id, 'Активных ключей нет!')

# Обработчик callback'ов для тарифов
@bot.callback_query_handler(func=lambda callback: callback.data in ['300', '1500', '2800'])
def handle_paid_key(callback):

    bot.send_message(admin_id, 'Выбрал тариф +1')

    price = callback.data

    user_key_id = f'{user_id(callback)}'

    # Создание ссылки на оплату
    invoice_link = invoice_management.create_invoice(int(price))
    if outline.user_key_info(user_key_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Оплатить', url=invoice_link[0]))
        
        # Кнопка "Проверить оплату"
        markup.add(types.InlineKeyboardButton('Проверить оплату', callback_data=f'check_payment_{invoice_link[1]}'))
        msg = bot.send_message(callback.message.chat.id, f'Сумма оплаты: {price} рублей\n1 - Оплатить\n2 - Нажать проверить оплату', reply_markup=markup)
    else:
        bot.send_message(callback.message.chat.id,f'У вас уже имеется ключ, проверка /mykeys')
    # Отправка сообщения с суммой и кнопками

# Обработчик для проверки статуса оплаты
@bot.callback_query_handler(func=lambda callback: callback.data.startswith('check_payment_'))
def check_payment_status(callback):

    bot.send_message(admin_id, 'Проверил оплату +1')

    libel = callback.data.split('_')[2]  # Извлекаем метку
    test_libel = 'L8cD7cJhpM'
    user_key_id = f'{user_id(callback)}'

    first_name = callback.from_user.first_name
    last_name = callback.from_user.last_name
    
    # Проверка статуса оплаты (предполагается, что у вас есть метод для этого)
    payment_status = invoice_management.payment_verification(libel)

    if payment_status:

        bot.send_message(admin_id, 'Оплатил +1')
        
        key = outline.create_new_key(key_id=user_key_id, name=str(user_id(callback)))

        database.add_db(user_id(callback), first_name, last_name, key.access_url)
        start_at_timer.start_timer(user_id(callback))
        
        text_message = (f"Оплата подтверждена! Ваш ключ активирован.\n'Метка об оплате-{libel}\n```{key.access_url}```")
        bot.send_message(callback.message.chat.id, text_message,parse_mode='Markdown')
        
        # Удаление кнопок "Оплатить" и "Проверить оплату"
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=types.InlineKeyboardMarkup())

    else:
        bot.send_message(callback.message.chat.id, f'Оплата не найдена или не подтверждена. Попробуйте позже.')





# Запуск бота
bot.polling(non_stop=True)
