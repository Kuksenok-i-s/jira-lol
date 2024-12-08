# main.py

from services.config import Config
from services.jira_service import JiraService
from services.utils import Utils
from services.chatgpt_service import ChatGPTService
from services.db_service import DBService
from services.telegram_service import TelegramService

def main():
    config = Config("config.yaml")
    jira = JiraService(config.jira_url, config.jira_user, config.jira_token, config.jira_query)
    utils = Utils()
    chatgpt = ChatGPTService(config.chatgpt_token)
    db = DBService(config.db_path)
    telegram = TelegramService(config.telegram_token, config.telegram_chat_id)
    
    db.init_db()
    table = utils.dry_run(jira, utils, config, chatgpt)
    print(table)
    # После проверки dry run - можно включить реальный лог
    # utils.log_time(jira, utils, config, chatgpt, db)
    # telegram.send_message("Время залогировано")

if __name__ == "__main__":
    main()
