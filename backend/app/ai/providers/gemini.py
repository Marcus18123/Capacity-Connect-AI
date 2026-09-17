import google.generativeai as genai
from typing import TypeVar, Type
from pydantic import BaseModel
import json
from .base import AIProvider

T = TypeVar("T", bound=BaseModel)

class GeminiProvider(AIProvider):
    """Google Gemini AI Provider Implementation."""

    def __init__(self, model_name: str = "gemini-1.5-pro", api_key: str = None):
        super().__init__(model_name, api_key)
        if self.api_key:
            genai.configure(api_key=self.api_key)

    async def generate_structured(self, prompt: str, schema: Type[T], system_instruction: str = "") -> T:
        if not self.api_key:
            raise ValueError("AI_API_KEY is not set.")
            
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Provide the schema structure in the prompt to guide the LLM
        schema_dict = schema.model_json_schema()
        full_prompt = f"{prompt}\n\nYou MUST return a JSON object that perfectly adheres to this JSON schema:\n{json.dumps(schema_dict, indent=2)}"
        
        response = await model.generate_content_async(full_prompt)
        
        # Validate and return
        try:
            parsed_json = json.loads(response.text)
            return schema(**parsed_json)
        except Exception as e:
            raise ValueError(f"Failed to parse Gemini output to schema: {e}\nOutput: {response.text}")

    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        if not self.api_key:
            raise ValueError("AI_API_KEY is not set.")
            
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction
        )
        
        response = await model.generate_content_async(prompt)
        return response.text

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            # Simple list models to verify auth
            models = genai.list_models()
            for m in models:
                if m.name == f"models/{self.model_name}":
                    return True
            return True
        except Exception:
            return False
