from abc import ABC, abstractmethod
import openai
from src.core.config import settings
from typing import List
from src.analysis.models import Issue
from src.llm.prompts import create_issue_explanation_prompt


class LLMClient(ABC):
    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass


class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE,
        )

    def get_completion(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior software engineer and static analysis expert.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content or ""


def get_llm_client() -> LLMClient:
    return OpenAIClient()
