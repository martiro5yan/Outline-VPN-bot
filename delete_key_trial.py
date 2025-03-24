import requests
import sys
import outline



print('удаление ключа')

user_id = sys.argv[1]

API_TOCEN = '7240622500:AAFL01ogk2InUs8ZFe077KicEO6URWHFpdk'
message = "Ваш пробный период завершен, ключ удален. Однако у вас есть 50% скидка на первый месяц использования\n /start для обновления цены"

url = f'https://api.telegram.org/bot{API_TOCEN}/sendMessage'

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