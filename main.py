#!/usr/bin/env python3
import argparse

from config import Config
from services.jira_service.jira_service import JiraService
from utils.utils import Utils
from services.chat_gpt_service.chat_gpt_service import ChatGPTService
from services.db_service.db_service import DBService
from services.telegram_service.bot import TelegramService


def run_actions(mode: str, use_default: bool, config: Config, jira: JiraService, utils: Utils, chatgpt: ChatGPTService, db, telegram):
    if mode == "dry-run":
        table = utils.dry_run(jira, utils, config, chatgpt, use_default)
        print(table)
    elif mode == "run":
        utils.log_time(jira, utils, config, chatgpt, db, use_default)
        telegram.send_message("Time logged.")


def main():
    parser = argparse.ArgumentParser(description="Jira time logger")
    parser.add_argument("mode", choices=["run", "dry-run", "telegram-bot"], help="Mode of operation")
    parser.add_argument("--use-default-tasks", action="store_true", help="Include default tasks")
    args = parser.parse_args()

    config = Config("config.yaml")
    jira = JiraService(config.jira_url, config.jira_user, config.jira_token)
    chatgpt = ChatGPTService(config.chatgpt_token)
    utils = Utils()
    db = DBService(config.db_path)
    telegram = TelegramService(config)

    db.init_db()

    if args.mode in ["run", "dry-run"]:
        run_actions(args.mode, args.use_default_tasks, config, jira, utils, chatgpt, db, telegram)
    elif args.mode == "telegram-bot":
        telegram.listen(utils, config, chatgpt, db)


if __name__ == "__main__":
    main()
