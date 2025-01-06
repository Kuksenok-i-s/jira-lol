# services/utils.py
import random
from prettytable import PrettyTable
from services.jira_service.jira_service import JiraHandler


class Utils:
    def __init__(self):
        pass

    def get_random_time_entries(self, total_hours):
        entries = []
        remaining = total_hours * 60
        while remaining > 0:
            chunk = random.randint(30, 90)
            if chunk > remaining:
                chunk = remaining
            entries.append(chunk)
            remaining -= chunk
        return entries

    def get_mr_info(self, issue_key: str) -> dict:
        return {"repo": "some-repo", "commits": ["commit1", "commit2"]}
