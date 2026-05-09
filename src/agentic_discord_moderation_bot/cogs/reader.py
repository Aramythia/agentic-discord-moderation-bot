import discord
from discord.ext import commands

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot
from agentic_discord_moderation_bot.utils.graph import create_graph


class Reader(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.graph = create_graph(bot.ai.llm)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        print(f"Message from {message.author}: {message.content}")
        result = await self.graph.ainvoke({"message_ctx": message})
        print(result)
        await message.reply(result["response"])
        

def setup(bot: discord.Bot):
    bot.add_cog(Reader(bot))
