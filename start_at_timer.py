import os
import requests


def start_timer(user_id):
    print('Старт таймера')
    os.system(f"echo 'python delete_key_and_subscription.py {user_id}' | at now +1 minute")

# def create_notification(user_id):
#     os.system(f"echo ")