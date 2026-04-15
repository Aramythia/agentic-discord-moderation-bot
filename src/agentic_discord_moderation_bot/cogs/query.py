from pprint import pprint
from typing import Annotated, List

import discord
from discord.ext import commands

from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool, InjectedToolArg

from pydantic import BaseModel, Field

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot


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


class Query(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.tools = [get_user_history]
        self.llm_with_tools = self.bot.ai.llm.bind_tools([get_user_history])
        self.tool_map = {t.name: t for t in self.tools}

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Limit your response to at most 30 words."),
            ("human", "{question}")
        ])

        self.query_chain = prompt | self.bot.ai.llm | StrOutputParser()

    @commands.slash_command(description="Query the bot with a question")
    @discord.option("question", description="The question you want to ask the bot")
    async def query(self, ctx: discord.ApplicationContext, *, question: str):
        response = await self.query_chain.ainvoke({"question": question})
        await ctx.respond(response)

    @commands.slash_command(description="Query the bot with a question and allow it to use tools")
    @discord.option("question", description="The question you want to ask the bot")
    async def query_with_tool(self, ctx: discord.ApplicationContext, *, question: str):
        await ctx.defer()
        messages = [
            SystemMessage(content="You are a helpful assistant. Limit your response to at most 30 words. If a user asks for information about another user, the user ID tends to be provided as a number like so: <@user_id>"),
            HumanMessage(content=question)
        ]

        for _ in range(3):
            response = await self.llm_with_tools.ainvoke(messages)
            messages.append(response)

            if not response.tool_calls:
                break

            for tool_call in response.tool_calls:
                tool_func = self.tool_map.get(tool_call['name'])
                if tool_func:
                    tool_result = await tool_func.ainvoke({**tool_call['args'], "ctx": ctx})
                    messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call['id']))
        
        await ctx.respond(response.content)


def setup(bot: discord.Bot):
    bot.add_cog(Query(bot))