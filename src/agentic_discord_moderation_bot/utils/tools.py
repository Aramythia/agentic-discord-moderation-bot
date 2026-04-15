from typing import Annotated, List

import discord

from langchain_core.tools import tool, InjectedToolArg
from pydantic import BaseModel, Field


class UserHistory(BaseModel):
    user_id: int = Field(description="An 18-digit integer representing the ID of the user to get history for")


@tool(args_schema=UserHistory)
async def get_user_history(ctx: Annotated[discord.ApplicationContext, InjectedToolArg], user_id: int) -> List[str]:
    """Get the last 5 messages from a user in the server."""
    messages = []
    async for msg in ctx.channel.history(limit=50):
        if msg.author.id == user_id:
            messages.append(msg.content)
            if len(messages) == 5:
                break
    return messages