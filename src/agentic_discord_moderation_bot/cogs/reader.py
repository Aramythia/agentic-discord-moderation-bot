import discord
from discord.ext import commands

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot


class Reader(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        print(f"Message from {message.author}: {message.content}")
        

def setup(bot: discord.Bot):
    bot.add_cog(Reader(bot))
