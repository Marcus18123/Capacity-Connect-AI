import pytest
from app.ai.providers.mock import MockAIProvider
from app.ai.schemas.skill_extraction import SkillExtractionResult
from app.ai.schemas.skill_gap import SkillGapAnalysisResult

@pytest.mark.asyncio
async def test_mock_provider_structured():
    provider = MockAIProvider()
    result = await provider.generate_structured("Extract Python", SkillExtractionResult)
    assert isinstance(result, SkillExtractionResult)
    # The mock fallback populates list fields with []
    assert isinstance(result.skills, list)

@pytest.mark.asyncio
async def test_mock_provider_gap():
    provider = MockAIProvider()
    result = await provider.generate_structured("Analyze gap", SkillGapAnalysisResult)
    assert isinstance(result, SkillGapAnalysisResult)
    assert result.target_role == "Mock target_role"
