from sqlalchemy.orm import Session
from src.data import models as db_models
from src.analysis import models as analysis_models


def create_repository(db: Session, name: str) -> db_models.Repository:
    db_repo = db_models.Repository(name=name)
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo


def save_analysis_result(
    db: Session, repo_id: int, analysis_result: analysis_models.AnalysisResult
):
    for file_analysis in analysis_result.files:
        db_file = db_models.File(
            repository_id=repo_id,
            file_path=file_analysis.file_path,
            loc=file_analysis.loc,
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        for issue in file_analysis.issues:
            db_issue = db_models.Issue(
                file_id=db_file.id,
                line_number=issue.line_number,
                code=issue.code,
                message=issue.message,
            )
            db.add(db_issue)

        for func_metrics in file_analysis.functions:
            db_func = db_models.Function(
                file_id=db_file.id,
                name=func_metrics.name,
                loc=func_metrics.loc,
                cyclomatic_complexity=func_metrics.cyclomatic_complexity,
                nesting_depth=func_metrics.nesting_depth,
                num_arguments=func_metrics.num_arguments,
            )
            db.add(db_func)
    db.commit()
