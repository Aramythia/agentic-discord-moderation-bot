from typing import Literal
from pydantic import BaseModel, Field


class ModerationFlag(BaseModel):
    verdict: Literal['clean', 'flagged']
    reason: str = Field(description='Brief explanation of the decision')
    confidence: float = Field(ge=0.0, le=1.0, description='Certainty score, 0 to 1')


class TriageDecision(BaseModel):
    path: Literal['question', 'moderation_command', 'none'] = Field(
        description=(
            "'question' if the message is asking something that warrants a helpful reply, "
            "'moderation_command' if it is instructing the bot to take a moderation action, "
            "'none' if the message requires no bot action."
        )
    )
    confidence: float = Field(ge=0.0, le=1.0, description='Certainty score, 0 to 1')