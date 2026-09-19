import asyncio
import json
from typing import TypeVar, Type
from pydantic import BaseModel
from .base import AIProvider

T = TypeVar("T", bound=BaseModel)

class MockAIProvider(AIProvider):
    """Domain-aware deterministic Mock AI Provider for development and fallback."""

    def __init__(self, model_name: str = "mock-model", api_key: str = None):
        super().__init__(model_name, api_key)

    async def generate_structured(self, prompt: str, schema: Type[T], system_instruction: str = "") -> T:
        await asyncio.sleep(0.1) # Simulate slight network latency
        
        schema_name = schema.__name__
        
        # 1. Skill Gap Analysis Result
        if schema_name == "SkillGapAnalysisResult":
            return schema(
                target_role=self._extract_target_role(prompt),
                overall_alignment_percentage=68.5,
                gaps=[
                    {
                        "competency_id": "gap-1",
                        "competency_name": "Autonomous Multi-Agent Swarms",
                        "gap_levels": 2.5,
                        "priority": "HIGH",
                        "priority_reason": "Critical gap for Senior Architect role. Requires hands-on experience with orchestration frameworks like LangGraph and AutoGen."
                    },
                    {
                        "competency_id": "gap-2",
                        "competency_name": "SQL & Query Optimization",
                        "gap_levels": 1.0,
                        "priority": "MEDIUM",
                        "priority_reason": "Prerequisite for scalable data retrieval in enterprise RAG pipelines."
                    }
                ]
            )


        # 2. Learning Path Result
        if schema_name == "LearningPathResult":
            target_role = self._extract_target_role(prompt)
            return schema(
                target_role=target_role,
                recommendations=[
                    {
                        "course_id": "c-101",
                        "course_title": "Production LLM Systems & Agentic Workflows",
                        "target_competency_id": "gap-1",
                        "reason": "Directly bridges your highest priority gap in Autonomous Multi-Agent Swarms.",
                        "priority": 1,
                        "estimated_duration_hours": 12.0,
                        "prerequisites_met": True
                    },
                    {
                        "course_id": "c-102",
                        "course_title": "Advanced SQL & Semantic Caching",
                        "target_competency_id": "gap-2",
                        "reason": "Addresses secondary gap in data retrieval performance.",
                        "priority": 2,
                        "estimated_duration_hours": 6.5,
                        "prerequisites_met": True
                    }
                ]
            )

        # 3. Skill Extraction Result
        if schema_name == "SkillExtractionResult":
            return schema(
                extracted_skills=[
                    {"skill": "Python", "confidence": 0.95, "evidence": "Python programming"},
                    {"skill": "Machine Learning", "confidence": 0.90, "evidence": "trained ML models"},
                    {"skill": "SQL", "confidence": 0.85, "evidence": "complex SQL queries"}
                ]
            )

        # 4. Competency Mapping Result
        if schema_name == "CompetencyMappingResult":
            return schema(
                mappings=[
                    {"raw_skill": "Python", "competency_id": "comp-python", "competency_name": "Python", "confidence": 0.95, "status": "MAPPED"},
                    {"raw_skill": "SQL", "competency_id": "comp-sql", "competency_name": "SQL", "confidence": 0.90, "status": "MAPPED"}
                ]
            )

        # Fallback default generation
        mock_data = self._generate_mock_data_for_schema(schema)
        return schema(**mock_data)

    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        await asyncio.sleep(0.1)
        if "next" in prompt.lower() or "recommend" in prompt.lower():
            return "Based on your current profile, focusing on Autonomous Multi-Agent Swarms will yield the highest impact on your competency alignment."
        return "I have analyzed your request based on your current competency profile and target role goals."

    async def health_check(self) -> bool:
        return True
        
    def _extract_target_role(self, prompt: str) -> str:
        if "Target Role:" in prompt:
            lines = prompt.split("\n")
            for line in lines:
                if "Target Role:" in line:
                    return line.replace("Target Role:", "").strip()
        return "Senior AI Solutions Architect"

    def _generate_mock_data_for_schema(self, schema: Type[T]) -> dict:
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
                mock_data[field_name] = f"Mock {field_name}"
                
        return mock_data
