import os
import requests



def start_timer_trial(user_id):
    if str(user_id) == '395838481':
        print('Старт таймера на админа')
        os.system(f"echo 'python3 delete_key_trial.py {user_id}' | at now +1 minute")
    else:
        os.system(f"echo 'python3 delete_key_trial.py {user_id}' | at now +3 days")

def start_timer(user_id,subscription_period):
    print('Старт таймера')
    os.system(f"echo 'python3 delete_key_and_subscription.py {user_id}' | at now +{subscription_period} days")

# def create_notification(user_id):
#     os.system(f"echo ")