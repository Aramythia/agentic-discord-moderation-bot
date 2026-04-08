import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot instance
bot = discord.Bot()

# Slash command: ping
@bot.slash_command(guild_ids=[331126066850824192], description="Ping the bot to check if it's online")
async def ping(ctx):
    await ctx.respond("Pong!")

# Message listener skeleton
@bot.listen('on_message')
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # TODO: Add your agentic AI logic here
    # This is where you would process messages and respond with LangChain/LangGraph
    print(f"Message from {message.author}: {message.content}")

    # Example: You could trigger AI responses based on message content
    # if some_condition:
    #     response = await generate_ai_response(message.content)
    #     await message.channel.send(response)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
