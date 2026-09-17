import json
from sqlalchemy.orm import Session
from app.ai.providers import get_ai_provider
from app.ai.schemas.competency_mapping import CompetencyMappingResult
from app.ai.prompts.prompts import COMPETENCY_MAPPING_SYSTEM
from app.ai.retrieval.competency_retriever import CompetencyRetriever

class CompetencyMappingService:
    @staticmethod
    async def map_skills(db: Session, extracted_skills: list[str]) -> CompetencyMappingResult:
        taxonomy = CompetencyRetriever.get_all_competencies(db)
        
        provider = get_ai_provider()
        prompt = f"""
        Map these extracted skills: {json.dumps(extracted_skills)}
        
        To the following official taxonomy:
        {json.dumps(taxonomy)}
        """
        
        result = await provider.generate_structured(
            prompt=prompt,
            schema=CompetencyMappingResult,
            system_instruction=COMPETENCY_MAPPING_SYSTEM
        )
        return result
