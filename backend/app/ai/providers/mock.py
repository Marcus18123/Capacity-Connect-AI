import asyncio
from typing import TypeVar, Type
from pydantic import BaseModel
from .base import AIProvider

T = TypeVar("T", bound=BaseModel)

class MockAIProvider(AIProvider):
    """Deterministic Mock AI Provider for testing and development."""

    def __init__(self, model_name: str = "mock-model", api_key: str = None):
        super().__init__(model_name, api_key)
        # We can store predefined mock responses based on schema names
        self.mock_responses = {}

    async def generate_structured(self, prompt: str, schema: Type[T], system_instruction: str = "") -> T:
        await asyncio.sleep(0.5) # Simulate network latency
        
        schema_name = schema.__name__
        
        # Default fallback mock data generation
        mock_data = self._generate_mock_data_for_schema(schema)
        
        return schema(**mock_data)

    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        await asyncio.sleep(0.5)
        return "This is a mock AI response. The provider is running in development mode."

    async def health_check(self) -> bool:
        return True
        
    def _generate_mock_data_for_schema(self, schema: Type[T]) -> dict:
        """Naively generates mock data based on field types to satisfy validation."""
        mock_data = {}
        for field_name, field_info in schema.model_fields.items():
            field_type = str(field_info.annotation).lower()
            
            if 'list' in field_type:
                mock_data[field_name] = []
            elif 'int' in field_type:
                mock_data[field_name] = 1
            elif 'float' in field_type:
                mock_data[field_name] = 0.95
            elif 'bool' in field_type:
                mock_data[field_name] = True
            else:
                # Default string
                mock_data[field_name] = f"Mock {field_name}"
                
        return mock_data
