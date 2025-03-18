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

API_TOCEN = '7240622500:AAFL01ogk2InUs8ZFe077KicEO6URWHFpdk'
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
    bot.send_message(admin_id, f'START +1 @{username(message)}')

    user_tg_id = message.chat.id
    if database.user_exists(user_tg_id) and database.can_use_discount(user_tg_id):
        price_month = '145'
        start_message =  text.discount_month
    else:
        price_month = '290'
        start_message =  text.start_message
    if invoice_management.check_token_validity():
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Попробовать бесплатно', callback_data='trial'))
        markup.add(types.InlineKeyboardButton(f'Нидерланды: 1 месяц {price_month} ₽', callback_data=price_month))
        markup.add(types.InlineKeyboardButton('Нидерланды: 1 год 2900 ₽', callback_data='2900'))
        markup.add(types.InlineKeyboardButton('Инструкция', callback_data='instruction'))
        markup.add(types.InlineKeyboardButton('Техподдержка', url='https://t.me/vpnytSupport_bot'))

        bot.send_message(message.chat.id, start_message, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сервис временно не доступен')
        bot.send_message(admin_id, 'Ошибка с токеном Yoomany')
        #Запись пользователей
        txt_manager.save_failed_ids(user_id(message))


@bot.callback_query_handler(func=lambda callback: callback.data == 'trial')
def trial(callback):
    if database.is_user_in_db_trial(callback.message.chat.id):
        bot.send_message(callback.message.chat.id, 'Вы уже использовали пробный период!')
    else:
        
        bot.send_message(admin_id, f'Активировал пробный период +1 @{username(callback)}')
        database.add_user_to_trial(callback.message.chat.id)
        user_key_id = f'{user_id(callback)}'
        if outline.user_key_info(user_key_id):
            key = outline.create_new_key(key_id=user_key_id, name=str(user_id(callback)))

            text_message = (f"У вас есть 3 дня пробного периода!\n\n```{key.access_url}```")
            bot.send_message(callback.message.chat.id, text_message,parse_mode='Markdown')
            print(user_id(callback),type(user_id(callback)))
            start_at_timer.start_timer_trial(user_id(callback))
        else:
            bot.send_message(callback.message.chat.id,f'У вас уже имеется ключ, проверка /mykeys')

# Обработчик команды /manual
@bot.message_handler(commands=['manual'])
def manual_links(user):
    bot.send_message(admin_id, f'MANUAL +1 @{username(user)}')
    bot.send_message(user.chat.id, text.instruction_text, parse_mode='Markdown')

# Обработчик для кнопки "Инструкция"
@bot.callback_query_handler(func=lambda callback: callback.data == 'instruction')
def send_help(callback):
    bot.send_message(admin_id, f'INSTRU +1 @{username(callback)}')
    bot.send_message(callback.message.chat.id, text.instruction_text, parse_mode='Markdown')

@bot.message_handler(commands=['mykeys'])
def return_user_keys(callback):
    
    bot.send_message(admin_id, f'MYKEYS +1 @{username(callback)}')

    id = user_id(callback)
    
    user = database.get_last_subscription(str(id))
    if user:
        key_name = user[0]
        subscription_end = user[1]
        key = user[2]

        if key == None:
            key = f"Активного ключа нет!"
        else:
            key = f"*Ключ:*```{key}```"
    
        response_message = (f"*Окончание подписки:*\n{subscription_end}\n\n"
                    f"*Имя ключа:* ({key_name})\n\n"
                    f"{key}"
        )
        bot.send_message(callback.chat.id, response_message, parse_mode='Markdown')
    else:
        bot.send_message(callback.chat.id, 'Активных ключей нет!')

# Обработчик callback'ов для тарифов
@bot.callback_query_handler(func=lambda callback: callback.data in ['290', '2900'])
def handle_paid_key(callback):
    handle_paid_key.price = callback.data

    bot.send_message(admin_id, f'Выбрал тариф {handle_paid_key.price} @{username(callback)}')

    

    user_key_id = f'{user_id(callback)}'

    # Создание ссылки на оплату
    invoice_link = invoice_management.create_invoice(int(handle_paid_key.price))
    if outline.user_key_info(user_key_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Оплатить', url=invoice_link[0]))
        
        # Кнопка "Проверить оплату"
        markup.add(types.InlineKeyboardButton('Проверить оплату', callback_data=f'check_payment_{invoice_link[1]}'))
        msg = bot.send_message(callback.message.chat.id, f'Сумма оплаты: {handle_paid_key.price} рублей\n1 - Оплатить\n2 - Нажать проверить оплату', reply_markup=markup)
    else:
        bot.send_message(callback.message.chat.id,f'У вас уже имеется ключ, проверка /mykeys')
    # Отправка сообщения с суммой и кнопками

# Обработчик для проверки статуса оплаты
@bot.callback_query_handler(func=lambda callback: callback.data.startswith('check_payment_'))
def check_payment_status(callback):
    user_key_id = f'{user_id(callback)}'

    bot.send_message(admin_id, f'Проверил оплату +1 @{username(callback)}')

    libel = callback.data.split('_')[2]  # Извлекаем метку
    test_libel = 'L8cD7cJhpM'
    
    if user_key_id == '395838481' or user_key_id == '441164668':
        libel = 'L8cD7cJhpM'#TEST
    else:
        libel = callback.data.split('_')[2]


    first_name = callback.from_user.first_name
    last_name = callback.from_user.last_name
    
    if handle_paid_key.price == '290':
        subscription_period = '31'
    elif handle_paid_key.price == '2900':
        subscription_period = '365'


    # Проверка статуса оплаты (предполагается, что у вас есть метод для этого)
    payment_status = invoice_management.payment_verification(libel)

    if payment_status:
        if database.user_exists(user_id(callback)):
            database.update_trial_status(user_id(callback))
            
        bot.send_message(admin_id, f'Оплатил +1 @{username(callback)}')
        
        key = outline.create_new_key(key_id=user_key_id, name=str(user_id(callback)))
        if database.is_user_in_db(user_id(callback)):
            database.update_purchased_key(user_id(callback),key.access_url,int(subscription_period))
            text_message = (f"Оплата подтверждена! Ваш ключ обновлен,вставте его в приложении Outline\n\n'Метка об оплате-{libel}\n\n```{key.access_url}```")
            bot.send_message(callback.message.chat.id, text_message,parse_mode='Markdown')
            start_at_timer.start_timer(user_id(callback),subscription_period)
        else:    
            database.add_db(user_id(callback), first_name, last_name, key.access_url,int(subscription_period))
            start_at_timer.start_timer(user_id(callback),subscription_period)
            text_message = (f"Оплата подтверждена! Ваш ключ активирован.\n'Метка об оплате-{libel}\n```{key.access_url}```")
            bot.send_message(callback.message.chat.id, text_message,parse_mode='Markdown')
        
        # Удаление кнопок "Оплатить" и "Проверить оплату"
        bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=types.InlineKeyboardMarkup())

    else:
        bot.send_message(callback.message.chat.id, f'Оплата не найдена или не подтверждена. Попробуйте через пару минут.')





# Запуск бота
bot.polling(non_stop=True)
