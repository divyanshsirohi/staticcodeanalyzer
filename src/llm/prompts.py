from typing import List
from src.analysis.models import Issue


def create_issue_explanation_prompt(issue: Issue) -> str:
    return f"""
    Explain why the following code issue is problematic and suggest a refactoring idea.
    Issue: {issue.message}
    Code: {issue.code}
    Line: {issue.line_number}
    """


def create_issue_clustering_prompt(issues: List[Issue]) -> str:
    issue_descriptions = "\n".join(
        [f"- {i.message} at {i.code}:{i.line_number}" for i in issues]
    )
    return f"""
    Given the following list of issues, cluster them into recurring themes and provide a high-level summary.
    Issues:
    {issue_descriptions}
    """
