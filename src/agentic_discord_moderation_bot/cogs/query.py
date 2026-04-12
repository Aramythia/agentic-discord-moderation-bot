import discord
from discord.ext import commands

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot


class Query(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot

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


def setup(bot: discord.Bot):
    bot.add_cog(Query(bot))