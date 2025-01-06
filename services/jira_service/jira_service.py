import random
from jira import JIRA
from services.config import Config
from services.jira_service.jql_builder import JQLBuilder
from services.jira_service.basic_classes import IssueData, JiraMessage, get_issue_data


class JiraService:
    def __init__(self, url, user, token):
        self.url = url
        self.user = user
        self.token = token
        self.jira = JIRA(server=self.url, basic_auth=(self.user, self.token))

    def add_worklog(self, issue_key, time_spent, comment) -> None:
        self.jira.add_worklog(issue=issue_key, timeSpent=time_spent, comment=comment)

    def add_comment(self, issue_key: str = None, comment: str = None) -> None:
        self.jira.add_comment(issue=issue_key, body=comment)

    def search_issues(self, jql: str, max_results: int = 50) -> None:
        return self.jira.search_issues(jql, maxResults=max_results)

    def create_issue(self, issue_data: dict):
        return self.jira.create_issue(fields=issue_data)

    def transition_issue(self, issue_key: str, transition_id: str) -> None:
        self.jira.transition_issue(issue=issue_key, transition=transition_id)

    def assign_issue(self, issue_key: str, assignee: str):
        self.jira.assign_issue(issue=issue_key, assignee=assignee)

    def edit_comment(self, issue_key: str, comment_id: str, new_text: str) -> None:
        comment_obj = self.jira.comment(issue_key, comment_id)
        comment_obj.update(body=new_text)

    def delete_comment(self, issue_key: str, comment_id: str) -> None:
        comment_obj = self.jira.comment(issue_key, comment_id)
        comment_obj.delete()  # it has that method but but ide messed this up

    def get_worklogs(self, issue_key: str):
        return self.jira.worklogs(issue_key)

    def attach_file(self, issue_key: str, file_path: str):
        self.jira.add_attachment(issue=issue_key, attachment=file_path)


class JiraHandler:
    def __init__(
        self,
        js: JiraService,
        config: Config,
        git_summary: dict[str, str],
    ) -> None:
        self.jira_service = js
        self.config = config
        self.git_summary = git_summary

    def get_in_progress_issues(self):
        jql = JQLBuilder().status("In Progress").build()
        return self.jira_service.search_issues(jql)

    def get_in_progress_issues_by_assignee(self, assignee: str) -> None:
        jql = JQLBuilder().status("In Progress").assignee(assignee).build()
        return self.jira_service.search_issues(jql)

    def get_unresolved_issues_by_project(self, project_key: str) -> None:
        jql = JQLBuilder().project(project_key).resolution_empty().build()
        return self.jira_service.search_issues(jql)

    def create_issue(self, project_key: str, summary: str, description: str) -> None:
        issue_data = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
        }
        return self.jira_service.create_issue(issue_data)

    def transition_issue(self, issue_key: str, transition_id: str, comment: str = None) -> None:
        if comment:
            self.jira_service.add_comment(issue_key, comment)
        self.jira_service.transition_issue(issue_key, transition_id)

    def assign_issue(self, issue_key: str, assignee: str) -> None:
        self.jira_service.assign_issue(issue_key, assignee)

    def add_comment(self, issue_key: str, comment: str) -> None:
        self.jira_service.add_comment(issue_key, comment)

    def add_worklog(self, issue_key: str, time_spent: str, comment: str) -> None:
        self.jira_service.add_worklog(issue_key, time_spent, comment)

    def log_random_worklog(self, issue_key: str) -> None:
        hours = random.randint(self.config.time_min, self.config.time_max)
        comment = f"Logged {hours}h"
        self.jira_service.add_worklog(issue_key, f"{hours}h", comment)


class JiraWorklogHandler:
    def __init__(self, jira_handler: JiraHandler) -> None:
        self.jira_handler = jira_handler

    def log_random(self, issue_key: str) -> None:
        self.jira_handler.log_random_worklog(issue_key)

    def log_worklog(self, issue_key: str, hours: str, comment: str) -> None:
        self.jira_handler.add_worklog(issue_key, hours, comment)

    def log_worklog_from_message(self, message: JiraMessage) -> None:
        issue_key = message.issue_key
        hours = message.hours
        comment = message.comment
        self.jira_handler.add_worklog(issue_key, hours, comment)

    def get_tasks(self) -> list[IssueData]:
        issues = self.jira_handler.get_in_progress_issues_by_assignee(self.jira_handler.config.jira_user)
        issues = [get_issue_data(issue) for issue in issues]
        return issues

    def get_tasks_by_project(self, project_key: str) -> list[IssueData]:
        issues = self.jira_handler.get_unresolved_issues_by_project(project_key)
        issues = [get_issue_data(issue) for issue in issues]
        return issues
