from yoomoney import Client, Quickpay ,exceptions
from threading import Timer
from dotenv import load_dotenv
import os

import random_generator

YOOMANY_TOCEN = os.getenv('YOOMANY_TOCEN')

client = Client(YOOMANY_TOCEN)


def check_token_validity():
    try:
        user_info = client.account_info()
          # Проверка валидности токена
        return True
    except exceptions.InvalidToken:
        return False

def payment_verification(label_line):
        history = client.operation_history(label=label_line)
        for operation in history.operations:
                print("\tМетка     -->", operation.label)
                print("\tСтатус     -->", operation.status)
                print("\tСумма перевода     -->", operation.amount)
                if operation.status == 'success':
                      return operation.amount
                else:
                      return False

# def start_payment_check(label_line):
#         chek = Timer(600,lambda: payment_verification(label_line))
#         chek.start()
#         chek.join()
#         if payment_successful:
#                return True
#         else:
#                return False


def create_invoice(price):
    label = random_generator.generate_random_string()
    quickpay = Quickpay(
            receiver="4100117442611660",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=price,
            label=label
            )
    return quickpay.redirected_url,label

# Получение списка операций (переводов)
# history = client.operation_history()

#     # Печать информации о каждой операции
# for operation in history.operations:
#       print(operation.label)

#print(create_invoice(150))