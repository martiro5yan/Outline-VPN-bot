import requests
import sys
import outline
import database




user_id = sys.argv[1]

API_TOCEN = '7240622500:AAFL01ogk2InUs8ZFe077KicEO6URWHFpdk'
message = "Ваша подписка окончена, ключ удален!"

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
    database.clear_purchased_key_by_id(user_id)
else:
    print(f"Ошибка: {response.status_code}, {response.text}")