# services/utils.py
import random
import prettytable

class Utils:
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

    def get_mr_info(self, issue_key):
        return {
            "repo": "some-repo",
            "commits": ["commit1", "commit2"]
        }

    def gather_issues(self, jira, use_default, config):
        issues = jira.get_inprogress_issues()
        if use_default:
            # Add default tasks as pseudo issues
            for task in config.default_tasks:
                # Mock object-like structure with required attributes
                class MockIssue:
                    def __init__(self, key):
                        self.key = key
                issues.append(MockIssue(task))
        return issues

    def dry_run(self, jira, utils, config, chatgpt, use_default):
        issues = self.gather_issues(jira, use_default, config)
        table = prettytable.PrettyTable(["Issue", "Time Entries (minutes)", "Repo", "Commits"])
        for issue in issues:
            total_hours = random.randint(config.time_min, config.time_max)
            entries = utils.get_random_time_entries(total_hours)
            mr_info = utils.get_mr_info(issue.key)
            table.add_row([issue.key, ", ".join(map(str, entries)), mr_info["repo"], ", ".join(mr_info["commits"])])
        return table

    def log_time(self, jira, utils, config, chatgpt, db, use_default):
        issues = self.gather_issues(jira, use_default, config)
        for issue in issues:
            total_hours = random.randint(config.time_min, config.time_max)
            entries = utils.get_random_time_entries(total_hours)
            mr_info = utils.get_mr_info(issue.key)
            comment = chatgpt.describe_commits(mr_info["commits"])
            for e in entries:
                h = e // 60
                m = e % 60
                time_str = f"{h}h {m}m" if h > 0 else f"{m}m"
                jira.add_worklog(issue.key, time_str, comment)
                db.insert_log(issue.key, time_str, comment)
