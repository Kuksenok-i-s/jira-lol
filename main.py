# main.py
import argparse
from services.config import Config
from services.jira_service import JiraService
from services.utils import Utils
from services.chatgpt_service import ChatGPTService
from services.db_service import DBService
from services.telegram_service import TelegramService

def run_actions(mode, use_default, config, jira, utils, chatgpt, db, telegram):
    if mode == "dry-run":
        table = utils.dry_run(jira, utils, config, chatgpt, use_default)
        print(table)
        telegram.send_message("Dry run completed.")
    elif mode == "run":
        utils.log_time(jira, utils, config, chatgpt, db, use_default)
        telegram.send_message("Time logged.")

def main():
    parser = argparse.ArgumentParser(description="Jira time logger")
    parser.add_argument("mode", choices=["run", "dry-run", "telegram-bot"], help="Mode of operation")
    parser.add_argument("--use-default-tasks", action="store_true", help="Include default tasks")
    args = parser.parse_args()

    config = Config("config.yaml")
    # jira = JiraService(config.jira_url, config.jira_user, config.jira_token, config.jira_query)
    utils = Utils()
    chatgpt = ChatGPTService(config.chatgpt_token)
    db = DBService(config.db_path)
    telegram = TelegramService(config)

    db.init_db()

    if args.mode in ["run", "dry-run"]:
        run_actions(args.mode, args.use_default_tasks, config, jira, utils, chatgpt, db, telegram)
    elif args.mode == "telegram-bot":
        telegram.listen(utils, config, chatgpt, db)

if __name__ == "__main__":
    main()
