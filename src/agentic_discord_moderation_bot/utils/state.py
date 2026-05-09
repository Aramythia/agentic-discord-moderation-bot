import discord
from langgraph.graph import MessagesState

from agentic_discord_moderation_bot.utils.model import ModerationFlag


class BasicBotState(MessagesState):
    message_ctx: discord.Message
    moderation_flag: ModerationFlag
    is_question: bool
    needs_internet: bool
    is_command: bool
    response: str
