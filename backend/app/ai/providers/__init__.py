from app.core.config import settings
from .base import AIProvider
from .mock import MockAIProvider
from .gemini import GeminiProvider

def get_ai_provider() -> AIProvider:
    provider_name = settings.AI_PROVIDER.lower()
    
    if provider_name == "gemini":
        return GeminiProvider(
            model_name=settings.AI_MODEL, 
            api_key=settings.AI_API_KEY
        )
    elif provider_name == "mock":
        return MockAIProvider(model_name="mock-ai")
    else:
        # Default fallback
        return MockAIProvider(model_name="fallback-mock-ai")
