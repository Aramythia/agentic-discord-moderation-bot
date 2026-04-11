import discord
from typing import List


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