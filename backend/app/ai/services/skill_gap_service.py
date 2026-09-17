import json
from sqlalchemy.orm import Session
from app.ai.providers import get_ai_provider
from app.ai.schemas.skill_gap import SkillGapAnalysisResult, GapReasoning
from app.ai.prompts.prompts import SKILL_GAP_SYSTEM
from app.ai.retrieval.competency_retriever import CompetencyRetriever
from app.models.user_competency import UserCompetency

class SkillGapService:
    @staticmethod
    async def analyze_gap(db: Session, trainee_id: str, target_role: str) -> SkillGapAnalysisResult:
        # Deterministic part: retrieve data
        role_reqs = CompetencyRetriever.get_role_requirements(db, target_role)
        
        user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == trainee_id).all()
        user_profile = {str(c.competency_id): c.proficiency_level for c in user_comps}
        
        # Calculate raw gaps (Deterministic)
        raw_gaps = []
        for req in role_reqs:
            curr_level = user_profile.get(req["competency_id"], 0.0)
            if curr_level < req["required_level"]:
                raw_gaps.append({
                    "competency_id": req["competency_id"],
                    "competency_name": req["competency_name"],
                    "gap": req["required_level"] - curr_level,
                    "importance": req["importance"]
                })
        
        if not raw_gaps:
            return SkillGapAnalysisResult(target_role=target_role, overall_alignment_percentage=100.0, gaps=[])

        # AI part: explain and prioritize
        provider = get_ai_provider()
        prompt = f"""
        Target Role: {target_role}
        Raw Calculated Gaps: {json.dumps(raw_gaps)}
        
        Explain why these gaps exist and assign a priority (LOW, MEDIUM, HIGH, CRITICAL).
        """
        
        result = await provider.generate_structured(
            prompt=prompt,
            schema=SkillGapAnalysisResult,
            system_instruction=SKILL_GAP_SYSTEM
        )
        return result
