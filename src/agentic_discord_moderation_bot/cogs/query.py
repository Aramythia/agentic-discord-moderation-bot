import discord
from discord.ext import commands

from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage, ToolMessage

from agentic_discord_moderation_bot.utils.AgentBot import AgentBot
from agentic_discord_moderation_bot.utils.tools import get_user_history, get_context


class Query(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.tools = [get_user_history, get_context]
        self.query_agent = create_agent(
            self.bot.ai.llm,
            tools=self.tools,
            system_prompt="You are a helpful assistant. Limit your response to at most 30 words.",
            debug=True
        )
        self.llm_with_tools = self.bot.ai.llm.bind_tools([get_user_history, get_context])
        self.tool_map = {t.name: t for t in self.tools}

    @commands.slash_command(description="Query the bot with a question")
    @discord.option("question", description="The question you want to ask the bot")
    async def query(self, ctx: discord.ApplicationContext, *, question: str):
        await ctx.defer()
        result = await self.query_agent.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            config={"configurable": {"ctx": ctx}},
        )
        response = result["messages"][-1].content if result.get("messages") else "No response generated."
        await ctx.respond(response)

    @commands.slash_command(description="Query the bot with a question and allow it to use tools")
    @discord.option("question", description="The question you want to ask the bot")
    async def query_with_tool(self, ctx: discord.ApplicationContext, *, question: str):
        await ctx.defer()
        messages = [
            SystemMessage(content="You are a helpful assistant. Limit your response to at most 30 words. If a user asks for information about another user, the user ID tends to be provided as a number like so: <@user_id>"),
            HumanMessage(content=question)
        ]

        for _ in range(3):
            response = await self.llm_with_tools.ainvoke(messages)
            messages.append(response)

            if not response.tool_calls:
                break

            for tool_call in response.tool_calls:
                tool_func = self.tool_map.get(tool_call['name'])
                if tool_func:
                    tool_result = await tool_func.ainvoke({**tool_call['args']}, config={"configurable": {"ctx": ctx}})
                    messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call['id']))
        
        await ctx.respond(response.content)


def setup(bot: discord.Bot):
    bot.add_cog(Query(bot))