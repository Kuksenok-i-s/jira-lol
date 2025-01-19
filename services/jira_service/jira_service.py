import random
from jira import JIRA
from config import Config
from services.jira_service.jql_builder import JQLBuilder


class JiraService:
    def __init__(self, url, user, token):
        self.url = url
        self.user = user
        self.token = token
        self.jira = JIRA(server=self.url, basic_auth=(self.user, self.token))

    def add_worklog(self, issue_key, time_spent, comment):
        self.jira.add_worklog(issue=issue_key, timeSpent=time_spent, comment=comment)

    def add_comment(self, issue_key: str = None, comment: str = None):
        self.jira.add_comment(issue=issue_key, body=comment)

    def search_issues(self, jql: str, max_results: int = 50):
        return self.jira.search_issues(jql, maxResults=max_results)

    def create_issue(self, issue_data: dict):
        return self.jira.create_issue(fields=issue_data)

    def transition_issue(self, issue_key: str, transition_id: str):
        self.jira.transition_issue(issue=issue_key, transition=transition_id)

    def assign_issue(self, issue_key: str, assignee: str):
        self.jira.assign_issue(issue=issue_key, assignee=assignee)

    def edit_comment(self, issue_key: str, comment_id: str, new_text: str):
        comment_obj = self.jira.comment(issue_key, comment_id)
        comment_obj.update(body=new_text)

    def delete_comment(self, issue_key: str, comment_id: str):
        comment_obj = self.jira.comment(issue_key, comment_id)
        comment_obj.delete()

    def get_worklogs(self, issue_key: str):
        return self.jira.worklogs(issue_key)

    def attach_file(self, issue_key: str, file_path: str):
        self.jira.add_attachment(issue=issue_key, attachment=file_path)


class JiraHandler:
    def __init__(self, js: JiraService, config: Config, git_summary: dict[str, str]):
        self.jira_service = js
        self.config = config
        self.git_summary = git_summary

    def get_in_progress_issues(self):
        jql = JQLBuilder().status("In Progress").build()
        return self.jira_service.search_issues(jql)

    def get_in_progress_issues_by_assignee(self, assignee: str):
        jql = JQLBuilder().status("In Progress").assignee(assignee).build()
        return self.jira_service.search_issues(jql)

    def get_unresolved_issues_by_project(self, project_key: str):
        jql = JQLBuilder().project(project_key).resolution_empty().build()
        return self.jira_service.search_issues(jql)

    def create_issue(self, project_key: str, summary: str, description: str):
        issue_data = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
        }
        return self.jira_service.create_issue(issue_data)

    def transition_issue(self, issue_key: str, transition_id: str, comment: str = None):
        if comment:
            self.jira_service.add_comment(issue_key, comment)
        self.jira_service.transition_issue(issue_key, transition_id)

    def assign_issue(self, issue_key: str, assignee: str):
        self.jira_service.assign_issue(issue_key, assignee)

    def add_comment(self, issue_key: str, comment: str):
        self.jira_service.add_comment(issue_key, comment)

    def add_worklog(self, issue_key: str, time_spent: str, comment: str):
        self.jira_service.add_worklog(issue_key, time_spent, comment)

    def log_random_worklog(self, issue_key: str):
        hours = random.randint(self.config.time_min, self.config.time_max)
        comment = f"Randomly logged {hours}h"
        self.jira_service.add_worklog(issue_key, f"{hours}h", comment)
