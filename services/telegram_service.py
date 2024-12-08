# services/telegram_service.py
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random

class TelegramService:
    def __init__(self, token, chat_id, config):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id
        self.config = config
        self.updater = Updater(token=token, use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("dry_run", self.cmd_dry_run))
        dp.add_handler(CommandHandler("run", self.cmd_run))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.on_message))

    def send_message(self, text):
        self.bot.send_message(chat_id=self.chat_id, text=text)

    def listen(self, jira, utils, config, chatgpt, db):
        self.jira = jira
        self.utils = utils
        self.config = config
        self.chatgpt = chatgpt
        self.db = db
        self.updater.start_polling()
        self.updater.idle()

    def cmd_dry_run(self, update, context):
        table = self.utils.dry_run(self.jira, self.utils, self.config, self.chatgpt, False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Dry run:\n{table}")

    def cmd_run(self, update, context):
        self.utils.log_time(self.jira, self.utils, self.config, self.chatgpt, self.db, False)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Time logged.")

    def on_message(self, update, context):
        text = update.message.text
        if "dry run" in text.lower():
            table = self.utils.dry_run(self.jira, self.utils, self.config, self.chatgpt, True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Dry run with default tasks:\n{table}")
        elif "run" in text.lower():
            self.utils.log_time(self.jira, self.utils, self.config, self.chatgpt, self.db, True)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Time logged with default tasks.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Команда не распознана.")
