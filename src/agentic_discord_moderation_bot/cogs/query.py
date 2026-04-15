import discord
from discord.ext import commands

from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage, ToolMessage

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot
from agentic_discord_moderation_bot.utils.tools import get_user_history, get_context


class Query(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.tools = [get_user_history, get_context]
        self.query_agent = create_agent(
            self.bot.ai.llm,
            tools=self.tools,
            system_prompt="You are a helpful assistant. Limit your response to at most 30 words.",
            debug=True
        )
        self.llm_with_tools = self.bot.ai.llm.bind_tools([get_user_history, get_context])
        self.tool_map = {t.name: t for t in self.tools}

    @commands.slash_command(description="Query the bot with a question")
    @discord.option("question", description="The question you want to ask the bot")
    async def query(self, ctx: discord.ApplicationContext, *, question: str):
        await ctx.defer()
        result = await self.query_agent.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            config={"recursion_limit": 10, "configurable": {"ctx": ctx}},
        )
        response = result["messages"][-1].content if result.get("messages") else "No response generated."
        await ctx.respond(response)


def setup(bot: discord.Bot):
    bot.add_cog(Query(bot))