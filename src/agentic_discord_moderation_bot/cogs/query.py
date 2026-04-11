import discord
from discord.ext import commands
from agentic_discord_moderation_bot.AgentBot import AgentBot


class Query(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot

    @commands.slash_command(description="Query the bot with a question")
    @discord.option("question", description="The question you want to ask the bot")
    async def query(self, ctx: discord.ApplicationContext, *, question: str):
        response = f"You asked: {question}"
        await ctx.respond(response)


def setup(bot: discord.Bot):
    bot.add_cog(Query(bot))