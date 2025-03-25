import http.server
import ssl
import json
import telebot
import os
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv('config.env')
BOT_TOKEN = os.getenv('TELEGRAM_TOCEN')

bot = telebot.TeleBot(BOT_TOKEN)

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Читаем данные из запроса
        length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json.loads(request_data))
        
        # Обрабатываем обновления в боте
        bot.process_new_updates([update])

        # Отправляем ответ 200 OK
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

# Настройки Webhook-сервера
HOST = "0.0.0.0"  # Принимает соединения со всех IP
PORT = 8443       # Порт Webhook

httpd = http.server.HTTPServer((HOST, PORT), WebhookHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="webhook.pem", keyfile="webhook.key", server_side=True)

print(f"🔹 Webhook-сервер запущен на {HOST}:{PORT} (HTTPS)")
httpd.serve_forever()
