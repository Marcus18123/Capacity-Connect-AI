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
        total_required_weight = 0.0
        achieved_weight = 0.0

        for req in role_reqs:
            curr_level = user_profile.get(req["competency_id"], 0.0)
            required_level = req["required_level"]
            importance = req.get("importance", 1.0) or 1.0
            
            total_required_weight += importance
            achieved_ratio = min(curr_level / required_level, 1.0) if required_level > 0 else 1.0
            achieved_weight += achieved_ratio * importance

            if curr_level < required_level:
                raw_gaps.append({
                    "competency_id": req["competency_id"],
                    "competency_name": req["competency_name"],
                    "gap": round(required_level - curr_level, 2),
                    "current_level": curr_level,
                    "required_level": required_level,
                    "importance": importance
                })

        overall_alignment = round((achieved_weight / total_required_weight) * 100, 2) if total_required_weight > 0 else 100.0

        if not raw_gaps:
            return SkillGapAnalysisResult(
                target_role=target_role, 
                overall_alignment_percentage=overall_alignment, 
                gaps=[]
            )

        # AI part: explain and prioritize
        provider = get_ai_provider()
        prompt = f"""
        Target Role: {target_role}
        Raw Calculated Gaps: {json.dumps(raw_gaps)}
        
        Explain why these gaps exist and assign a priority (LOW, MEDIUM, HIGH, CRITICAL).
        """
        
        try:
            result = await provider.generate_structured(
                prompt=prompt,
                schema=SkillGapAnalysisResult,
                system_instruction=SKILL_GAP_SYSTEM
            )
            result.target_role = target_role
            result.overall_alignment_percentage = overall_alignment
            return result
        except Exception as e:
            # Safe fallback if AI provider throws unexpected exception
            gap_reasonings = []
            for g in raw_gaps:
                priority = "HIGH" if g["gap"] >= 2.0 else "MEDIUM" if g["gap"] >= 1.0 else "LOW"
                gap_reasonings.append(
                    GapReasoning(
                        competency_id=str(g["competency_id"]),
                        competency_name=g["competency_name"],
                        gap_score=g["gap"],
                        priority=priority,
                        ai_explanation=f"Required level is {g['required_level']} but current level is {g['current_level']}."
                    )
                )
            return SkillGapAnalysisResult(
                target_role=target_role,
                overall_alignment_percentage=overall_alignment,
                gaps=gap_reasonings
            )

