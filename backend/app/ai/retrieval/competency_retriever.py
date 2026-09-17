from sqlalchemy.orm import Session
from app.models.competency import Competency
from app.models.role import Role, RoleCompetency
from typing import List, Dict

class CompetencyRetriever:
    @staticmethod
    def get_all_competencies(db: Session) -> List[dict]:
        comps = db.query(Competency).all()
        return [{"id": str(c.id), "name": c.name, "category": c.category, "level": c.level.value} for c in comps]
        
    @staticmethod
    def get_role_requirements(db: Session, role_name: str) -> List[dict]:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            return []
        
        reqs = []
        for rc in role.role_competencies:
            reqs.append({
                "competency_id": str(rc.competency.id),
                "competency_name": rc.competency.name,
                "required_level": rc.required_level,
                "importance": rc.importance
            })
        return reqs
