from typing import List

import discord

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class UserHistory(BaseModel):
    user_id: int = Field(description="An 18-digit integer representing the ID of the user to get history for")


@tool(args_schema=UserHistory)
async def get_user_history(user_id: int, config: RunnableConfig) -> List[str]:
    """Get the last 5 messages from a user in the server."""
    ctx: discord.ApplicationContext = config["configurable"]["ctx"]
    messages = []
    async for msg in ctx.channel.history(limit=50):
        if msg.author.id == user_id:
            messages.append(msg.content)
            if len(messages) == 5:
                break
    return messages


@tool
async def get_context(config: RunnableConfig) -> str:
    """Get context surrounding the query: who asked it, and where. Returns a dictionary.
    
    Relevant Vocabulary:
    - author: the user who triggered the query; Keys: author_name, author_user_id
    - channel: the channel the query was triggered in; Keys: channel_name, channel_id, channel_topic, channel_is_nsfw
    - guild: the server the query was triggered in; Keys: guild_name, guild_id
    """
    ctx: discord.ApplicationContext = config["configurable"]["ctx"]
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