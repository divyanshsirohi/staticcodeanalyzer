from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.data.database import get_db
from src.data import repository as repo
from src.analysis.python_analyzer import PythonCodeAnalyzer
from src.analysis.sql_analyzer import SQLAnalyzer
from src.analysis.models import AnalysisResult, FileAnalysis
from src.evaluation.benchmark import create_synthetic_dataset
from src.evaluation.metrics import calculate_metrics, GROUND_TRUTH
from src.visualization.plots import generate_issue_frequency_chart
import os
import shutil
import zipfile
from typing import List, Dict, Set

router = APIRouter()


@router.post("/analyze", response_model=int)
async def analyze_repository(
    upload_file: UploadFile = File(...), db: Session = Depends(get_db)
):
    repo_name = (
        upload_file.filename.replace(".zip", "")
        if upload_file.filename
        else "uploaded_repo"
    )

    # Create a temporary directory to extract the zip file
    tmp_dir = f"temp_{repo_name}"
    os.makedirs(tmp_dir, exist_ok=True)

    with zipfile.ZipFile(upload_file.file, "r") as zip_ref:
        zip_ref.extractall(tmp_dir)

    # Start analysis
    file_analyses: List[FileAnalysis] = []
    for root, _, files in os.walk(tmp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".py"):
                analyzer = PythonCodeAnalyzer(file_path)
                file_analyses.append(analyzer.analyze())
            elif file.endswith(".sql"):
                analyzer = SQLAnalyzer(file_path)
                file_analyses.append(analyzer.analyze())

    analysis_result = AnalysisResult(repository_name=repo_name, files=file_analyses)

    # Save to DB
    db_repo = repo.create_repository(db, name=repo_name)
    repo.save_analysis_result(db, db_repo.id, analysis_result)

    # Cleanup
    shutil.rmtree(tmp_dir)

    return db_repo.id


@router.get("/results/{repo_id}")
def get_analysis_results(repo_id: int, db: Session = Depends(get_db)):
    db_repo = (
        db.query(repo.db_models.Repository)
        .filter(repo.db_models.Repository.id == repo_id)
        .first()
    )
    if not db_repo:
        return JSONResponse(
            status_code=404, content={"message": "Repository not found"}
        )
    return db_repo


@router.get("/evaluation")
def get_evaluation_metrics():
    create_synthetic_dataset()

    analysis_results: Dict[str, Set[str]] = {}

    for file_path in GROUND_TRUTH.keys():
        if file_path.endswith(".py"):
            analyzer = PythonCodeAnalyzer(file_path)
            analysis = analyzer.analyze()
            issues = {issue.message for issue in analysis.issues}
            for func in analysis.functions:
                issues.update({issue.message for issue in func.issues})
        elif file_path.endswith(".sql"):
            analyzer = SQLAnalyzer(file_path)
            analysis = analyzer.analyze()
            issues = {issue.message for issue in analysis.issues}
        else:
            issues = set()

        analysis_results[file_path] = issues

    metrics = calculate_metrics(analysis_results)
    return metrics


@router.get("/visualizations/{repo_id}")
def get_visualization(repo_id: int, db: Session = Depends(get_db)):
    chart_path = generate_issue_frequency_chart(db, repo_id)
    if not chart_path:
        return JSONResponse(
            status_code=404, content={"message": "No issues found to generate chart"}
        )

    return {"chart_url": f"/static/{os.path.basename(chart_path)}"}
