from typing import List, Dict, Set

# Ground truth for the synthetic dataset
GROUND_TRUTH = {
    "sample_test_repo/bad_code/god_function.py": {
        "Long parameter list",
        "God function (too long)",
        "Deeply nested function",
    },
    "sample_test_repo/bad_code/deep_nesting.py": {
        "Deeply nested function",
        "Dead code (unused function)",
    },
    "sample_test_repo/sql_files/queries.sql": {
        "Avoid using 'SELECT *'",
        "Missing WHERE clause in UPDATE/DELETE statement",
        "Hardcoded value in WHERE clause",
        "Potential nested subquery",
    },
    "sample_test_repo/clean_code/simple_app.py": set(),
}


def calculate_metrics(analysis_results: Dict[str, Set[str]]) -> Dict[str, float]:
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    all_possible_issues: Set[str] = set()
    for issues in GROUND_TRUTH.values():
        all_possible_issues.update(issues)

    for file_path, detected_issues in analysis_results.items():
        ground_truth_issues = GROUND_TRUTH.get(file_path, set())

        tp = len(detected_issues.intersection(ground_truth_issues))
        fp = len(detected_issues.difference(ground_truth_issues))
        fn = len(ground_truth_issues.difference(detected_issues))

        true_positives += tp
        false_positives += fp
        false_negatives += fn

    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0.0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0.0
    )
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }
