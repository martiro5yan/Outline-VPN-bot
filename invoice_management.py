from yoomoney import Client, Quickpay ,exceptions
from threading import Timer

import random_generator
y= '4100117442611660.4EC078D838C7468BFEC00E1171B2507EC5A0BB49C8E54643045E257F1BCDC06B2476895B547C7F0D40A8DA77D470B72BD7A1E9D0991F9D0CF14FD3FE1250BAD3265A91A80C937609B56B357C2CCBF8A74BDC43A83A4003C6098041BCAC1CD7437FAD676FCDE455377B17AE24E00A1AD9AA35D52147FAE8DB72AFAC4ABC70745A'


client = Client(y)


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