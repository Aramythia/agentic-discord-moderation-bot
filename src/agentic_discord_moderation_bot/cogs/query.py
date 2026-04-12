import discord
from discord.ext import commands
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agentic_discord_moderation_bot.utils.AgentBot import AgentBot


class Query(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot

    @commands.slash_command(description="Query the bot with a question")
    @discord.option("question", description="The question you want to ask the bot")
    async def query(self, ctx: discord.ApplicationContext, *, question: str):
        response = await self.bot.ai.llm.ainvoke([
            SystemMessage(content="You are a helpful assistant. Limit your response to at most 30 words."),
            HumanMessage(content=question)
        ])
        await ctx.respond(response.content)


def setup(bot: discord.Bot):
    bot.add_cog(Query(bot))