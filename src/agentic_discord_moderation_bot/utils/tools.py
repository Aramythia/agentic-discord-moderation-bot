from typing import Dict, List

import discord

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from pydantic import BaseModel, Field

_ddg_wrapper = DuckDuckGoSearchAPIWrapper(safesearch="off")
ddg_tool = DuckDuckGoSearchResults(
    description=(
        "A wrapper around DuckDuckGo search - a web search tool. "
        "Input is a plaintext string search query."
        "Use this tool if the user query is trying to 'google' something or "
        "search the web with any generic search engine."
        "Use this tool to get current information from the internet, "
        "e.g. specific video game details, recent events, restaurant reviews, etc. "
    ),
    api_wrapper=_ddg_wrapper,
    output_format="list",
)
wikipedia_query_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(),
    description=(
        "A tool to query Wikipedia for factual or encyclopedic information. "
        "Prefer this tool for reliable and well-sourced information, "
        "especially topics with high 'cultural capital', "
        "e.g. historical events, scientific concepts, notable figures, etc. "
    )
)


class UserHistory(BaseModel):
    user_id: int = Field(description="An 18-digit integer representing the ID of the user to get history for")


@tool(args_schema=UserHistory)
async def get_user_history(config: RunnableConfig, user_id: int) -> List[Dict[str, str]]:
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


class InviteParams(BaseModel):
    age: int = Field(
        description=(
            "After creation, the invite link will expire after this many seconds."), 
        gt=0,
        lt=604800,  # 7 days is 604800 seconds
        default=86400  # 24 hours is 86400 seconds
    )
    uses: int = Field(
        description="The maximum number of uses for the invite link.", 
        gt=0,
        lt=25,  # Arbitrary upper limit to prevent abuse
        default=5
    )


@tool(args_schema=InviteParams)
async def create_invite(config: RunnableConfig, age: int, uses: int) -> str:
    """Create an invite link for the channel the query was triggered in. Returns the invite URL as a string as well as the time it expires and the maximum number of uses."""
    ctx: discord.ApplicationContext = config["configurable"]["ctx"]
    invite = await ctx.channel.create_invite(max_age=age, max_uses=uses)
    return {
        "url": invite.url,
        "max_age": invite.expires_at if invite.expires_at else None,
        "max_uses": invite.max_uses,
    }