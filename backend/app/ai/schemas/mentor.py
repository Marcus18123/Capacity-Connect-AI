from pydantic import BaseModel, Field
from typing import List, Optional

class MentorInsight(BaseModel):
    topic: str
    insight: str
    action_item: Optional[str] = None

class MentorResponse(BaseModel):
    answer: str = Field(..., description="The conversational answer to the user's question.")
    insights: List[MentorInsight] = Field(default_factory=list, description="Any specific structured insights extracted from the context.")
    confidence: float = Field(..., description="Confidence that the answer is completely grounded in the provided platform data.")
