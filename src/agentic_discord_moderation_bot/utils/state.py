from typing import Optional
from langgraph.graph import MessagesState

from agentic_discord_moderation_bot.utils.model import ModerationFlag, TriageDecision


class BasicBotState(MessagesState):
    moderation_flag: Optional[ModerationFlag]
    triage_result: Optional[TriageDecision]
    is_question: Optional[bool]
    needs_internet: Optional[bool]
    is_command: Optional[bool]
    response: Optional[str]
