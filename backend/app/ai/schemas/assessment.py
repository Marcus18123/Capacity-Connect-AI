from pydantic import BaseModel, Field
from typing import List

class QuestionOption(BaseModel):
    id: str = Field(..., description="A, B, C, or D")
    text: str

class GeneratedQuestion(BaseModel):
    question_text: str
    options: List[QuestionOption] = Field(..., min_length=2, max_length=5)
    correct_option_id: str = Field(..., description="Must match one of the option IDs.")
    explanation: str = Field(..., description="Why the correct option is correct.")
    difficulty: str = Field(..., description="BEGINNER, INTERMEDIATE, ADVANCED, or EXPERT.")
    marks: int = Field(default=1)

class AssessmentGenerationResult(BaseModel):
    title: str
    competency_id: str
    questions: List[GeneratedQuestion]
    quality_score: float = Field(..., description="AI self-assessed quality score (0.0 to 1.0).")
