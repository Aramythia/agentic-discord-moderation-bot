import discord
import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_GUILDS = os.getenv('DEBUG_GUILDS', '').split(',')

class AgentBot(discord.Bot):
    def __init__(self, cogs: List[str] = None, *args, **kwargs):
        self.init_cogs = cogs or []
        super().__init__(*args, **kwargs)

        for cog in self.init_cogs:
            try:
                self.load_extension(cog)
                print(f"Loaded cog: {cog}")
            except Exception as e:
                print(f"Failed to load cog {cog}: {e}")

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        print(f"Message from {message.author}: {message.content}")

# Create bot instance
bot = AgentBot(intents=discord.Intents.all(), debug_guilds=DEBUG_GUILDS)

# Slash command: ping
@bot.slash_command(description="Ping the bot to check if it's online")
async def ping(ctx):
    await ctx.respond("Pong!")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
