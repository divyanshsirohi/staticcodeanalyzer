from typing import List, Optional
from pydantic import BaseModel


class Issue(BaseModel):
    code: str
    line_number: int
    message: str


class FunctionMetrics(BaseModel):
    name: str
    loc: int
    cyclomatic_complexity: int
    nesting_depth: int
    num_arguments: int
    issues: List[Issue]


class FileAnalysis(BaseModel):
    file_path: str
    loc: int
    functions: List[FunctionMetrics]
    issues: List[Issue]


class AnalysisResult(BaseModel):
    repository_name: str
    files: List[FileAnalysis]
