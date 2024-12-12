import random
from jira import JIRA
from config import Config


class JiraService:
    def __init__(self, url, user, token, query):
        self.url = url
        self.user = user
        self.token = token
        self.query = query
        self.jira = JIRA(server=self.url, basic_auth=(self.user, self.token))

    def get_in_progress_issues(self):
        return self.jira.search_issues(self.query)

    def add_worklog(self, issue_key, time_spent, comment):
        self.jira.add_worklog(issue=issue_key, timeSpent=time_spent, comment=comment)

    def add_comment(self, issue_key: str= None, comment: str= None): 
        self.jira.add_comment(issue=issue_key, body=comment)

class JiraHandler:
    def __init__(self, js: JiraService, config: Config, git_summary: dict[str, str]):
        self.jira_service = js
        self.config = config
        self.git_summary = git_summary

    def make_report_for_jira(self):
        in_progress_issues = self.jira_service.get_in_progress_issues()
        for issue in in_progress_issues:
            print(f"Issue: {issue.key}, Assignee: {issue.fields.assignee}, Status: {issue.fields.status}")
            self.jira_service.add_comment(issue.key, "")
            hours = random.randint(self.config.time_min, self.config.time_max)
            self.jira_service.add_worklog(issue.key, str(hours)+"h", "")

    def make_report_for_git(self):
        for key, value in self.git_summary.items():
            print(f"Git: {key}, Value: {value}")