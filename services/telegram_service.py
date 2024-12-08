# services/telegram_service.py

import telegram

class TelegramService:
    def __init__(self, token, chat_id):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def send_message(self, text):
        self.bot.send_message(chat_id=self.chat_id, text=text)
