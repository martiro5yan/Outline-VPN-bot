#!/usr/bin/env python3
from outline_vpn.outline_vpn import OutlineVPN
from dotenv import load_dotenv
import os
import sys



load_dotenv('config.env')
api_url = os.getenv("API_URL")
cert_sha256 = os.getenv('CERT_SHA256')

outline_manager = OutlineVPN(api_url=api_url, cert_sha256=cert_sha256)


def list_keys():
    keys = outline_manager.get_keys()
    for key in keys:
        print(f"key id: {key.key_id}")
        print(f"key name: {key.name}")
        print(f"used: {int(key.used_bytes)/ (1024**3):.2f} GB")
        print(f'key: {key.access_url}')
        print("-"*100)

def create_new_key():
    print('-- Создание ключа --')
    name = input("key name: ")
    id = input("key id: ")
    key = outline_manager.create_key(key_id=id, name=name)
    print(key.access_url)

def delete_key():
    print('-- Удаление ключа --')
    outline_manager.delete_key(input('key id: '))
    print('-- Ключ удален --')

dictionary_commands = {'listkeys':list_keys,
                       'createkey':create_new_key,
                       'deletekey':delete_key}

#list_keys()
#create_new_key()
#delete_key()
func_name = sys.argv[1]
if func_name in dictionary_commands:
    dictionary_commands[func_name]()
else:
    print('команды не существует')