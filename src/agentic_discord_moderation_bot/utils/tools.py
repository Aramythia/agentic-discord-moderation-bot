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


@tool
async def get_context(ctx: Annotated[discord.ApplicationContext, InjectedToolArg]) -> str:
    """Get context surrounding the query: who asked it, and where. Returns a dictionary.
    
    Relevant Vocabulary:
    - author: the user who triggered the query; Keys: author_name, author_user_id
    - channel: the channel the query was triggered in; Keys: channel_name, channel_id, channel_topic, channel_is_nsfw
    - guild: the server the query was triggered in; Keys: guild_name, guild_id
    """
    return {
        "author_name": ctx.author.display_name,
        "author_user_id": ctx.author.id,
        "channel_name": ctx.channel.name,
        "channel_id": ctx.channel_id,
        "channel_topic": ctx.channel.topic,
        "channel_is_nsfw": ctx.channel.is_nsfw(),
        "guild_name": ctx.guild.name,
        "guild_id": ctx.guild_id,
    }