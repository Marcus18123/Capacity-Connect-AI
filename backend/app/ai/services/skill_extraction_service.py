from sqlalchemy.orm import Session
from app.models.user_competency import UserCompetency
from app.ai.providers import get_ai_provider
from app.ai.schemas.skill_extraction import SkillExtractionResult
from app.ai.prompts.prompts import SKILL_EXTRACTION_SYSTEM

class SkillExtractionService:
    @staticmethod
    async def extract_skills(text: str) -> SkillExtractionResult:
        provider = get_ai_provider()
        prompt = f"Analyze the following resume or profile text and extract skills:\n\n{text}"
        
        result = await provider.generate_structured(
            prompt=prompt,
            schema=SkillExtractionResult,
            system_instruction=SKILL_EXTRACTION_SYSTEM
        )
        return result
