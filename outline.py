from outline_vpn.outline_vpn import OutlineVPN
import text
import requests
import time


api_url = 'https://80.85.246.132:14296/e7HnqgKgosHDiOZyX0892g'
cert_sha256 = 'BCC52A3156337F6AA6171DE7119E75C749B9DDB7CFAEFC35B1CC6A24078CF6A6'

client = OutlineVPN(api_url=api_url, cert_sha256=cert_sha256)

gb = 1073741824


def delete_key(key_id: str):
    print('удалено')
    return client.delete_key(key_id)


def info_keys():
    return client.get_keys()

def delete_key(key_id: str):
    return client.delete_key(key_id)



def get_key_info(key_id):
    try:
        id = client.get_key(key_id)
    except Exception as e:
        # Можно также вывести сообщение об ошибке для отладки
        print(f"Error occurred: {e}")
        return False
    if id.key_id == key_id:
        return True
    else:
        return False


# Создание новго ключа
def create_new_key(key_id: str = None, name: str = None, data_limit_gb: float = None):
    return client.create_key(key_id=key_id, name=name)


def get_service_info():
    return client.get_server_information()

def create_keys_list(key_name):
    users_keys = []
    keys = info_keys()
    for key in keys:
        if key_name == key.name:
            users_keys.append(key.name)
    return users_keys


def user_key_info(key_name):
    keys = create_keys_list(key_name)
    if key_name in keys:
        return False
    else:
        return True
    

def get_keys_by_id(key_id):
    user_keys = []
    # Метод для получения информации о ключе по его ID
    keys = client.get_keys()  # Получение всех ключей
    for key in keys:
        if key.name == key_id:  # Сравниваем с переданным ID
            user_keys.append(key.name)
            user_keys.append(key.key_id)
            user_keys.append(key.access_url)
    return user_keys
    return None  # Если ключ не найден, возвращаем None

