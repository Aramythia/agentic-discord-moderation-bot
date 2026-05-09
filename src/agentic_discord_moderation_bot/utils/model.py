from typing import Literal
from pydantic import BaseModel, Field


class ModerationFlag(BaseModel):
    verdict: Literal['clean', 'flagged']
    reason: str = Field(description='Brief explanation of the decision')
    confidence: float = Field(ge=0.0, le=1.0, description='Certainty score, 0 to 1')