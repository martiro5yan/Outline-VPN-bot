#!/usr/bin/env python3
from outline_vpn.outline_vpn import OutlineVPN
from dotenv import load_dotenv
from colorama import Fore, Style, init
import os
import sys

# Инициализация colorama
init(autoreset=True)

def bytes_to_gb(bytes):
    if type(bytes) == int:
        result = bytes / (1024**3)
        return result
    else:
        return 0

def list_keys():
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Список ключей --")
    keys = outline_manager.get_keys()
    for key in keys:
        print(f"{Fore.CYAN}🔑 ID ключа: {Fore.YELLOW}{key.key_id}")
        print(f"{Fore.CYAN}📛 Имя ключа: {Fore.YELLOW}{key.name}")
        #print(type(key.used_bytes))
        print(f"{Fore.CYAN}📊 Использовано: {bytes_to_gb(key.used_bytes):.2f} GB")
        print(f"{Fore.CYAN}🔗 Ключ: {Fore.GREEN}{key.access_url}")
        print(f"{Fore.MAGENTA}{'-'*100}")


def create_new_key():
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Создание нового ключа --")
    name = input(f"{Fore.CYAN}Введите название ключа: {Fore.YELLOW}")
    id = input(f"{Fore.CYAN}Введите ID ключа: {Fore.YELLOW}")
    key = outline_manager.create_key(key_id=id, name=name)
    print(f"{Fore.GREEN}✅ Ключ создан! Ссылка доступа: {Style.BRIGHT}{key.access_url}")


def delete_key():
    print(f"{Style.BRIGHT}{Fore.RED}-- Удаление ключа --")
    key_id = input(f"{Fore.CYAN}Введите ID ключа для удаления: {Fore.YELLOW}")
    outline_manager.delete_key(key_id)
    print(f"{Fore.GREEN}🗑️ Ключ {key_id} успешно удалён.")
def stop_key():
    key_id = input('key_id: ')
    outline_manager.set_key_enabled(key_id, enabled=False)
    print("Ключ выключен")


def get_service_info():
    return outline_manager.get_server_information()

def key_info():
    key_id = input(f"{Fore.CYAN}Введите ID ключа: {Fore.YELLOW}")
    key=outline_manager.get_key(key_id)
    print(key.method)

def total_consumption():
    summ = 0
    keys = outline_manager.get_keys()
    print(f"{Fore.WHITE}NL-centOS-vdsina")
    # Заголовок таблицы
    print("-" * 70)
    print(f"{Style.BRIGHT + Fore.BLUE}{'Имя ключа':<25} {'Использовано (байт)':>20} {'Использовано (GB)':>20}")
    print("-" * 70)
    for key in keys:
        used = int(key.used_bytes) if key.used_bytes is not None else 0
        gb = bytes_to_gb(used)
        print(f"{key.name:<25} {used:>20,} {gb:>20.2f}")  # Числа с запятыми и выравниванием

        summ += used

    print("-" * 70)
    print(f"{Style.BRIGHT + Fore.BLUE}{'Итог:':<45} {bytes_to_gb(summ):>20.2f} GB")

#CENTOS_7
Centos_API_URL = 'https://80.85.246.132:14296/e7HnqgKgosHDiOZyX0892g'
Centos_CERT_SHA256 = 'BCC52A3156337F6AA6171DE7119E75C749B9DDB7CFAEFC35B1CC6A24078CF6A6'

#UBUNTU_24

Ubuntu_API_URL = 'https://195.133.14.151:64500/ZNqCQhSJpNk0pAIp_Q5pVQ'
Ubuntu_CERT_SHA256 = 'FD2F23E26F75B56C0540AC0436B648C1D688F92C1C86C887891EEEDFA9AE6D61'


# Словарь команд
dictionary_commands = {
    'lk': list_keys,
    'ck': create_new_key,
    'dk': delete_key,
    'info': get_service_info,
    'ki': key_info,
    'tc': total_consumption
}


def main(func_name):
    if func_name in dictionary_commands:
        dictionary_commands[func_name]()
    else:
        print(f"{Fore.RED}❌ Команда '{func_name}' не существует. Используйте: lk,ck,dk")

# Обработка команды из аргументов
if len(sys.argv) < 2:
    print(f"{Fore.RED}❌ Не указана команда. Доступные команды: lk,ck,dk")
    sys.exit(1)
try:
    server_name = sys.argv[1]
    func_name = sys.argv[2]
    if server_name == 'u':
        outline_manager = OutlineVPN(api_url=Ubuntu_API_URL, cert_sha256=Ubuntu_CERT_SHA256)
        main(func_name)
    elif server_name == 'c':
        outline_manager = OutlineVPN(api_url=Centos_API_URL, cert_sha256=Centos_CERT_SHA256)
        main(func_name)
except IndexError:
    print('Выберите сервер')




