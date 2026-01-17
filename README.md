# LLM-Powered Static Code Analyzer

This project is a static code analysis tool that uses rule-based detectors for Python and SQL, and then leverages a Large Language Model (LLM) to provide explanations and suggestions for the detected issues.

## Architecture

The application is built with a FastAPI backend and a modular architecture:

- **`src/analysis`**: Contains the core static analysis logic.
  - `python_analyzer.py`: Uses Python's `ast` module to parse code, extract metrics (LOC, complexity, etc.), and apply rules.
  - `sql_analyzer.py`: Uses regex to find common SQL anti-patterns.
- **`src/api`**: Defines the FastAPI endpoints for analyzing repositories, retrieving results, and viewing evaluations.
- **`src/core`**: Core configuration and settings.
- **`src/data`**: Handles database interactions.
  - `database.py`: SQLAlchemy setup and session management.
  - `models.py`: Database table definitions.
  - `repository.py`: Functions for saving and retrieving analysis data.
- **`src/llm`**: Manages interaction with the LLM.
  - `client.py`: Abstract base class for LLM clients and an OpenAI implementation.
  - `prompts.py`: Functions to generate prompts for the LLM.
- **`src/evaluation`**: Framework for evaluating the analyzer's performance.
  - `benchmark.py`: Creates a synthetic dataset of good and bad code.
  - `metrics.py`: Calculates precision, recall, and F1-score against a ground truth.
- **`src/visualization`**: Generates charts from the analysis data.
  - `plots.py`: Uses Matplotlib to create visualizations.
- **`src/main.py`**: The main entry point for the FastAPI application.

## How Precision is Measured

Precision is a measure of the accuracy of the positive predictions made by the analyzer. It is calculated as:

**Precision = True Positives / (True Positives + False Positives)**

- **True Positives (TP)**: The number of issues correctly identified by the analyzer that are actual issues (as defined in the ground truth).
- **False Positives (FP)**: The number of issues incorrectly identified by the analyzer that are not actual issues.

The ground truth is defined in `src/evaluation/metrics.py` for our synthetic benchmark dataset. The `/api/evaluation` endpoint runs the analyzer against this dataset and calculates the precision, recall, and F1-score.

## Limitations

- **Limited Language Support**: Currently only supports Python and basic SQL analysis.
- **Rule-Based Limitations**: The rule-based detectors are simple and may not catch all possible issues or may have false positives.
- **Dead Code Detection**: The current dead code detection is limited to unused functions within the same file and does not account for dynamic calls or calls from other files.
- **LLM Cost and Latency**: The LLM-powered explanations add cost and latency to the analysis process.
- **No Real-Time Analysis**: The analysis is done on a repository snapshot and is not real-time.

## How to Run Locally

1.  **Clone the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your_openai_api_key"
    ```
5.  **Run the FastAPI application:**
    ```bash
    uvicorn src.main:app --reload
    ```
6.  The API will be available at `http://127.0.0.1:8000`.

## Example API Usage

### Analyze a Repository

- **Endpoint**: `POST /api/analyze`
- **Body**: `multipart/form-data` with a `file` field containing a ZIP file of the repository.

Example using `curl`:
```bash
curl -X POST -F "upload_file=@/path/to/your/repo.zip" http://127.0.0.1:8000/api/analyze
```

### Get Analysis Results

- **Endpoint**: `GET /api/results/{repo_id}`

Example:
```bash
curl http://127.0.0.1:8000/api/results/1
```

### Get Evaluation Metrics

- **Endpoint**: `GET /api/evaluation`

Example:
```bash
curl http://127.0.0.1:8000/api/evaluation
```
