# services/jira_service.py
from jira import JIRA

class JiraService:
    def __init__(self, url, user, token, query):
        self.url = url
        self.user = user
        self.token = token
        self.query = query
        self.jira = JIRA(server=self.url, basic_auth=(self.user, self.token))

    def get_inprogress_issues(self):
        return self.jira.search_issues(self.query)

    def add_worklog(self, issue_key, time_spent, comment):
        self.jira.add_worklog(issue=issue_key, timeSpent=time_spent, comment=comment)
