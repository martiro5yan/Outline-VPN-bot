import os
from dotenv import load_dotenv

load_dotenv('config.env')

admin_id = os.getenv('TELEGRAM_ADMIN_ID')

def start_timer_trial(user_id):
    if str(user_id) == admin_id:
        print('Старт таймера на админа')
        os.system(f"echo 'python3 /home/martirosyan/Outline-VPN-bot/delete_key_trial.py {user_id}' | at now +1 minute")
    else:
        os.system(f"echo 'python3 /home/martirosyan/Outline-VPN-bot/delete_key_trial.py {user_id}' | at now +3 days")

def start_timer(user_id,subscription_period):
    if str(user_id) == admin_id:
        print('Старт таймера на админа')
        subscription_period = 1
        os.system(f"echo 'python3 /home/martirosyan/Outline-VPN-bot/delete_key_trial.py {user_id}' | at now +{subscription_period} minute")
    else:
        print('Старт таймера')
        os.system(f"echo 'python3 /home/martirosyan/Outline-VPN-bot/delete_key_trial.py {user_id}' | at now +{subscription_period} days")

# def create_notification(user_id):
#     os.system(f"echo ")