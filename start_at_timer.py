import os
import requests



def start_timer_trial(user_id):
    if user_id == '395838481':
        print('Старт таймера на админа')
        os.system(f"echo 'python delete_key_trial.py {user_id}' | at now +1 minute")
    else:
        os.system(f"echo 'python delete_key_trial.py {user_id}' | at now +1 days")

def start_timer(user_id):
    print('Старт таймера')
    os.system(f"echo 'python delete_key_and_subscription.py {user_id}' | at now +30 days")

# def create_notification(user_id):
#     os.system(f"echo ")