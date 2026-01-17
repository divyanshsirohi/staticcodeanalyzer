import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from src.data import models as db_models
from collections import Counter


def generate_issue_frequency_chart(db: Session, repo_id: int) -> str:
    issues = (
        db.query(db_models.Issue)
        .join(db_models.File)
        .filter(db_models.File.repository_id == repo_id)
        .all()
    )
    issue_counts = Counter(issue.message for issue in issues)

    if not issue_counts:
        return ""

    labels, values = zip(*issue_counts.items())

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values)
    plt.xlabel("Frequency")
    plt.title(f"Issue Frequency for Repository ID {repo_id}")
    plt.tight_layout()

    chart_path = f"charts/issue_frequency_repo_{repo_id}.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path
