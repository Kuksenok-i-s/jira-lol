import yaml

class Config:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.jira_url = data["jira"]["url"]
        self.jira_user = data["jira"]["user"]
        self.jira_token = data["jira"]["token"]
        self.time_min = data["time"]["min"]
        self.time_max = data["time"]["max"]
        self.telegram_token = data["telegram"]["token"]
        self.gitlab_api_url = data["gitlab"]["url"]
        self.gitlab_token = data["gitlab"]["token"]
        self.chatgpt_token = data["chatgpt"]["token"]
        self.db_path = data["database"]["path"]
        self.default_tasks = data.get("default_tasks", [])
