import ast
from typing import List, Dict, Any

# Assuming src.analysis.models is correctly defined as per previous steps
from src.analysis.models import FunctionMetrics, Issue, FileAnalysis


class PythonCodeAnalyzer(ast.NodeVisitor):
    """
    Analyzes a single Python file to extract metrics and identify issues.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.source_code = f.read()
            self.lines = self.source_code.splitlines()
        self.tree = ast.parse(self.source_code, filename=file_path)
        self.functions: List[FunctionMetrics] = []
        self.file_issues: List[Issue] = []

    def analyze(self) -> FileAnalysis:
        """
        Triggers the analysis of the file.
        """
        self.visit(self.tree)
        # Detect dead code (unused functions)
        self._detect_dead_code()
        return FileAnalysis(
            file_path=self.file_path,
            loc=len(self.lines),
            functions=self.functions,
            issues=self.file_issues,
        )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visit a function definition and extract metrics.
        """
        metrics = self._calculate_function_metrics(node)
        self.functions.append(metrics)
        self.generic_visit(node)

    def _calculate_function_metrics(self, node: ast.FunctionDef) -> FunctionMetrics:
        """
        Calculates metrics for a given function node.
        """
        loc = node.end_lineno - node.lineno if node.end_lineno else 0
        complexity = self._calculate_cyclomatic_complexity(node)
        nesting_depth = self._calculate_nesting_depth(node)
        num_args = len(node.args.args)

        issues = []
        if complexity > 10:
            issues.append(
                Issue(
                    code=node.name,
                    line_number=node.lineno,
                    message="High cyclomatic complexity",
                )
            )
        if loc > 50:
            issues.append(
                Issue(
                    code=node.name,
                    line_number=node.lineno,
                    message="God function (too long)",
                )
            )
        if nesting_depth > 4:
            issues.append(
                Issue(
                    code=node.name,
                    line_number=node.lineno,
                    message="Deeply nested function",
                )
            )
        if num_args > 5:
            issues.append(
                Issue(
                    code=node.name,
                    line_number=node.lineno,
                    message="Long parameter list",
                )
            )

        return FunctionMetrics(
            name=node.name,
            loc=loc,
            cyclomatic_complexity=complexity,
            nesting_depth=nesting_depth,
            num_arguments=num_args,
            issues=issues,
        )

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """
        Calculates cyclomatic complexity of a function.
        """
        complexity = 1
        for sub_node in ast.walk(node):
            if isinstance(
                sub_node,
                (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler),
            ):
                complexity += 1
        return complexity

    def _calculate_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """
        Calculates the maximum nesting depth of a node.
        """
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.AsyncWith)):
                max_depth = max(
                    max_depth, self._calculate_nesting_depth(child, current_depth + 1)
                )
            else:
                max_depth = max(
                    max_depth, self._calculate_nesting_depth(child, current_depth)
                )
        return max_depth

    def _detect_dead_code(self) -> None:
        """
        Detects unused functions within the file.
        """
        defined_functions = {f.name for f in self.functions}
        called_functions = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                called_functions.add(node.func.id)

        dead_functions = defined_functions - called_functions
        for func_metrics in self.functions:
            if func_metrics.name in dead_functions:
                self.file_issues.append(
                    Issue(
                        code=func_metrics.name,
                        line_number=next(
                            (
                                n.lineno
                                for n in ast.walk(self.tree)
                                if isinstance(n, ast.FunctionDef)
                                and n.name == func_metrics.name
                            ),
                            0,
                        ),
                        message="Dead code (unused function)",
                    )
                )
