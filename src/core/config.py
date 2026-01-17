from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    OPENAI_API_KEY: str = "your_openai_api_key"
    OPENAI_API_BASE: str = "https://api.openai.com/v1"

    class Config:
        env_file = ".env"


settings = Settings()
