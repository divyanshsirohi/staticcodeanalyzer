import re
from typing import List
from src.analysis.models import Issue, FileAnalysis


class SQLAnalyzer:
    """
    Analyzes a single SQL file to identify common issues.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.content = f.read()
            self.lines = self.content.splitlines()

    def analyze(self) -> FileAnalysis:
        """
        Triggers the analysis of the SQL file.
        """
        issues = self._find_issues()
        return FileAnalysis(
            file_path=self.file_path,
            loc=len(self.lines),
            functions=[],  # SQL files don't have functions in the same way Python does
            issues=issues,
        )

    def _find_issues(self) -> List[Issue]:
        """
        Finds issues in the SQL content using regex-based detectors.
        """
        issues = []

        # Rule 1: Detect SELECT *
        for i, line in enumerate(self.lines):
            if re.search(r"SELECT\s+\*", line, re.IGNORECASE):
                issues.append(
                    Issue(
                        code=line.strip(),
                        line_number=i + 1,
                        message="Avoid using 'SELECT *'",
                    )
                )

        # Rule 2: Missing WHERE clause in DELETE/UPDATE
        for i, line in enumerate(self.lines):
            if re.search(r"\b(UPDATE|DELETE)\b", line, re.IGNORECASE) and not re.search(
                r"\bWHERE\b", line, re.IGNORECASE
            ):
                issues.append(
                    Issue(
                        code=line.strip(),
                        line_number=i + 1,
                        message="Missing WHERE clause in UPDATE/DELETE statement",
                    )
                )

        # Rule 3: Detect nested subqueries (simple detection)
        for i, line in enumerate(self.lines):
            if len(re.findall(r"\bSELECT\b", line, re.IGNORECASE)) > 1:
                issues.append(
                    Issue(
                        code=line.strip(),
                        line_number=i + 1,
                        message="Potential nested subquery",
                    )
                )

        # Rule 4: Detect hardcoded values in WHERE clauses
        for i, line in enumerate(self.lines):
            if re.search(r'WHERE\s+\w+\s*=\s*[\'"]', line, re.IGNORECASE):
                issues.append(
                    Issue(
                        code=line.strip(),
                        line_number=i + 1,
                        message="Hardcoded value in WHERE clause",
                    )
                )

        return issues
