# jql_builder.py


class JQLBuilder:
    def __init__(self):
        self.conditions = []

    def status(self, status_value: str):
        self.conditions.append(f"status = '{status_value}'")
        return self

    def assignee(self, assignee_value: str):
        self.conditions.append(f"assignee = '{assignee_value}'")
        return self

    def project(self, project_key: str):
        self.conditions.append(f"project = '{project_key}'")
        return self

    def resolution_empty(self):
        self.conditions.append("resolution IS EMPTY")
        return self

    def text_search(self, text: str):
        self.conditions.append(f"(summary ~ '{text}' OR description ~ '{text}')")
        return self

    def build(self) -> str:
        if not self.conditions:
            return ""
        return " AND ".join(self.conditions)
