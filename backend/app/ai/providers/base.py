import os
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Any, Dict, Optional

T = TypeVar("T", bound=BaseModel)

class AIProvider(ABC):
    """Abstract Base Class for AI Providers."""
    
    def __init__(self, model_name: str, api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("AI_API_KEY", "")

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Type[T], system_instruction: str = "") -> T:
        """Generates structured output validated against a Pydantic schema."""
        pass

    @abstractmethod
    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """Generates raw text."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Validates if the provider is reachable and correctly configured."""
        pass
