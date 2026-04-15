from typing import Dict, List

import discord

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class UserHistory(BaseModel):
    user_id: int = Field(description="An 18-digit integer representing the ID of the user to get history for")


@tool(args_schema=UserHistory)
async def get_user_history(user_id: int, config: RunnableConfig) -> List[Dict[str, str]]:
    """Get the last 10 messages from a user in the server. Returns a list of dictionaries.
    
    Each dictionary represents a message and has the following content information:
    - content: the text content of the message
    - created_at: the timestamp of when the message was created in ISO format
    - message_id: the ID of the message, often used as an input for other commands
    - jump_url: a URL that can be used to jump to the message in Discord, used to provide users a link to the message
    """
    ctx: discord.ApplicationContext = config["configurable"]["ctx"]
    messages = []
    async for msg in ctx.channel.history(limit=100):
        if msg.author.id == user_id:
            msg_info = {
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "message_id": msg.id,
                "jump_url": msg.jump_url,
            }
            messages.append(msg_info)
            if len(messages) == 10:
                break
    return messages


@tool
async def get_context(config: RunnableConfig) -> Dict[str, str]:
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