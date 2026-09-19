import asyncio
import pytest
from app.ai.providers.mock import MockAIProvider
from app.ai.schemas.skill_extraction import SkillExtractionResult
from app.ai.schemas.skill_gap import SkillGapAnalysisResult

def test_mock_provider_structured():
    provider = MockAIProvider()
    result = asyncio.run(provider.generate_structured("Extract Python", SkillExtractionResult))
    assert isinstance(result, SkillExtractionResult)
    # The mock fallback populates list fields with []
    assert isinstance(result.skills, list)

def test_mock_provider_gap():
    provider = MockAIProvider()
    result = asyncio.run(provider.generate_structured("Analyze gap", SkillGapAnalysisResult))
    assert isinstance(result, SkillGapAnalysisResult)
    assert result.target_role == "Senior AI Solutions Architect"

