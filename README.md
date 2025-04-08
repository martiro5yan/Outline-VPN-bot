# Outline-VPN-bot
# Telegram VPN Bot

Этот проект представляет собой Telegram-бота для продажи VPN-доступа через Outline. Пользователи могут получить пробный период, приобрести различные тарифы, получить инструкции и управлять своими ключами. Проект интегрирован с платежной системой Yoomoney и использует базу данных для хранения информации о пользователях и подписках.

## 🧩 Функциональность

- 📲 Команда `/start`:
  - Приветствие пользователя и отображение тарифов.
  - Отображение спецпредложения для возвращающихся пользователей.
  - Кнопки для оплаты, пробного периода, инструкции и техподдержки.

- 🧪 Пробный период:
  - Пользователь может активировать пробный период (3 дня).
  - Проверка наличия активного ключа перед выдачей нового.

- 💳 Покупка подписки:
  - Поддерживаются тарифы: 1 день, 1 месяц, 1 год.
  - Генерация ссылки на оплату через Yoomoney.
  - Кнопка для проверки статуса оплаты.
  - Автоматическая активация ключа после подтверждения оплаты.

- 🧾 Команда `/mykeys`:
  - Получение текущего активного ключа.
  - Отображение даты окончания подписки.

- 📚 Команда `/manual` и кнопка "Инструкция":
  - Отправка текстовой инструкции по использованию VPN.

- 🛠️ Поддержка:
  - Ссылка на бот техподдержки.

## ⚙️ Технологии

- **Python 3.10+**
- **pyTelegramBotAPI** — работа с Telegram Bot API
- **dotenv** — хранение конфиденциальных переменных (`BOT_TOKEN`, `admin_id` и др.)
- **Outline API** — для создания и управления VPN-ключами
- **Yoomoney API** — для генерации и проверки счетов
- **Собственная база данных** — управление пользователями, пробными периодами и подписками

## 🔐 Переменные окружения (`config.env`)

```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_ADMIN_ID=your_telegram_id
TEST_LIBEL=your_test_payment_label
```

## 📁 Структура проекта

- `main.py` — основной файл бота
- `database.py` — работа с базой данных
- `outline.py` — взаимодействие с Outline API
- `invoice_management.py` — работа с Yoomoney
- `text.py` — тексты сообщений
- `start_at_timer.py` — запуск таймера подписки
- `txt_manager.py` — логирование и обработка ID пользователей

## 🚀 Запуск

1. Установите зависимости:
   ```bash
   pip install pyTelegramBotAPI python-dotenv
   ```
2. Создайте файл `.env` с конфигурацией.
3. Запустите бота:
   ```bash
   python main.py
   ```

## 📬 Обратная связь

По всем вопросам и предложениям: [@vpnytSupport_bot](https://t.me/vpnytSupport_bot)
