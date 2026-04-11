import discord
import os
from dotenv import load_dotenv
from agentic_discord_moderation_bot.AgentBot import AgentBot

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_GUILDS = os.getenv('DEBUG_GUILDS', '').split(',')

init_cogs = ["cogs.query"]
bot = AgentBot(cogs=init_cogs, intents=discord.Intents.all(), debug_guilds=DEBUG_GUILDS)

@bot.slash_command(description="Ping the bot to check if it's online")
async def ping(ctx):
    await ctx.respond("Pong!")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
