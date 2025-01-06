from dataclasses import dataclass
from jira import Issue


@dataclass
class IssueData:
    key: str
    summary: str
    status: str
    assignee: str
    reporter: str


@dataclass
class JiraMessage:
    issue_key: str
    hours: int
    comment: str


def get_issue_data(issue: Issue) -> IssueData:
    return IssueData(
        key=issue.key,
        summary=issue.fields.summary,
        status=issue.fields.status.name,
        assignee=issue.fields.assignee.displayName if issue.fields.assignee else None,
        reporter=issue.fields.reporter.displayName,
    )
