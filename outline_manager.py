#!/usr/bin/env python3
from outline_vpn.outline_vpn import OutlineVPN
from dotenv import load_dotenv
from colorama import Fore, Style, init
import os
import sys

# Инициализация colorama
init(autoreset=True)

# Загрузка переменных окружения
load_dotenv('config.env')
api_url = os.getenv("API_URL")
cert_sha256 = os.getenv('CERT_SHA256')

# Создание экземпляра OutlineVPN
outline_manager = OutlineVPN(api_url=api_url, cert_sha256=cert_sha256)


def list_keys():
    print(f"{Style.BRIGHT}{Fore.BLUE}-- Список ключей --")
    keys = outline_manager.get_keys()
    for key in keys:
        print(f"{Fore.CYAN}🔑 ID ключа: {Fore.YELLOW}{key.key_id}")
        print(f"{Fore.CYAN}📛 Имя ключа: {Fore.YELLOW}{key.name}")
        print(f"{Fore.CYAN}📊 Использовано: {Fore.YELLOW}{int(key.used_bytes) / (1024**3):.2f} GB")
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


# Словарь команд
dictionary_commands = {
    'listkeys': list_keys,
    'createkey': create_new_key,
    'deletekey': delete_key
}

# Обработка команды из аргументов
if len(sys.argv) < 2:
    print(f"{Fore.RED}❌ Не указана команда. Доступные команды: listkeys, createkey, deletekey")
    sys.exit(1)

func_name = sys.argv[1]
if func_name in dictionary_commands:
    dictionary_commands[func_name]()
else:
    print(f"{Fore.RED}❌ Команда '{func_name}' не существует. Используйте: listkeys, createkey, deletekey")
