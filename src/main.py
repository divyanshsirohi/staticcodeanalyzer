from fastapi import FastAPI
from src.api import endpoints
from src.data.database import engine, Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create a directory for charts
os.makedirs("charts", exist_ok=True)


app = FastAPI(
    title="LLM-Powered Static Code Analyzer",
    description="A static code analysis tool enhanced with LLM capabilities.",
    version="1.0.0",
)

app.include_router(endpoints.router, prefix="/api", tags=["analysis"])


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the LLM-Powered Static Code Analyzer API"}


# Example of how to serve static files (e.g., charts)
# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="charts"), name="static")
