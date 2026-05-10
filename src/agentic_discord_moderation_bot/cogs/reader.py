import discord
from discord.ext import commands

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot
from agentic_discord_moderation_bot.utils.graph import create_graph


class Reader(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.graph = create_graph(bot.ai.llm)
        print(self.graph.get_graph().draw_mermaid())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or message.author.bot:
            return
        
        result = await self.graph.ainvoke(
                {"messages": [message.content]},
                config={"configurable": {"message_ctx": message}},
            )
        if "response" in result:
            await message.reply(result["response"])
        print("="*40, "\n", f"Message from {message.author}: {message.content}", "\n", result, "\n", "="*40)
        

def setup(bot: discord.Bot):
    bot.add_cog(Reader(bot))
