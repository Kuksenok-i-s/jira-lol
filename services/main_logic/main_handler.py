from jira_service.jira_service import JiraService, JiraHandler


class ScenarioHandler:
    def __init__(self, jira_service: JiraService, jira_handler: JiraHandler):
        self.jira_service = jira_service
        self.jira_handler = jira_handler
