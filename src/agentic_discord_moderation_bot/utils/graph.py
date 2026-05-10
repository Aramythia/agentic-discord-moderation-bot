from typing import Literal

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from agentic_discord_moderation_bot.utils.state import BasicBotState
from agentic_discord_moderation_bot.utils.model import ModerationFlag, TriageDecision


# Functions
# moderation_check - flags messages that violate guidelines
# triage - determines which general workflow to follow (e.g. answer question, moderate, etc.)
# analyze_question - determines whether to answer a question directly or use tools
# analyze_moderation - determines which moderation actions to take, if any
# synthesize_response - generates a response to the user based on the current state


def create_graph(llm: BaseChatModel, checkpointer=None) -> CompiledStateGraph:
    """Build and compile the moderation graph with the given LLM.

    Parameters
    ----------
    llm : BaseChatModel
        The chat model to use in graph nodes.
    checkpointer : optional
        An optional checkpointer to save and load graph state.

    Returns
    -------
    CompiledStateGraph
        The compiled LangGraph ready for invocation.
    """
    moderation_llm = llm.with_structured_output(ModerationFlag)
    triage_llm = llm.with_structured_output(TriageDecision)
    questions_agent = create_agent(
            llm,
            tools=[TavilySearch(max_results=3, include_answer=True)],
            system_prompt=(
                "You are a helpful assistant tasked with answering general questions. "
                "Provide concise and accurate responses, using tools when necessary. "
                "Use Tavily search to find current or factual information. "
                "Limit answers to generally 30 words, up to 80 if the answer is complex."
            )
        )


    async def moderation_check(state: BasicBotState, config: RunnableConfig) -> BasicBotState:
        message_content = state["messages"][-1].content
        system = SystemMessage(
            content=(
                "You are a Discord moderation assistant. "
                "Determine whether the following message violates community guidelines. "
                "Provide a structured output with the verdict, reason, and confidence score."
            )
        )
        result: ModerationFlag = await moderation_llm.ainvoke([system, HumanMessage(content=message_content)])
        return {"moderation_flag": result}
    
    def route_moderation(state: BasicBotState) -> Literal["triage", "synthesize_response"]:
        flag: ModerationFlag = state["moderation_flag"]
        return "synthesize_response" if flag.verdict == "flagged" else "triage"


    async def triage(state: BasicBotState, config: RunnableConfig) -> dict:
        system = SystemMessage(
            content=(
                "You are a Discord bot assistant named Ganyu. A message has passed moderation and needs routing. "
                "Determine whether the message is a question directed at the bot that warrants a reply, "
                "a command instructing the bot to take a moderation action, "
                "or general chat that requires no bot action. "
                "A question is directed at the bot if it explicitly mentions the bot or is asking for general information. "
                "Examples: 'Hey Ganyu, can you help me with my homework?' -> question, mentions your name | "
                "'What is the capital of France?' -> question, general information | "
                "'Sean, do you know what time it is?' -> question, easily answerable by the bot despite naming someone else | "
                "'Where did you get that shirt?' -> none, likely directed at a human in the chat\n"
                "A command is an instruction for moderation action e.g. kicking, warning, timeout, ban, delete message, etc."
            )
        )
        result: TriageDecision = await triage_llm.ainvoke(
            [system, HumanMessage(content=state["messages"][-1].content)]
        )
        return {"triage_result": result}

    def route_triage(state: BasicBotState) -> Literal["analyze_question", "synthesize_response", "__end__"]:
        result = state["triage_result"]
        if result.path == "none" or result.confidence < 0.75:
            return END
        if result.path == "question":
            return "analyze_question"
        return "synthesize_response"  # moderation_command


    async def synthesize_response(state: BasicBotState) -> BasicBotState:
        state_summary = {
            k: (v.model_dump() if hasattr(v, "model_dump") else v)
            for k, v in state.items()
            if k != "messages"
        }
        system = SystemMessage(
            content=(
                "You are a Discord moderation assistant. "
                "Generate a concise, friendly reply to send to the user based on the conversation and state below. "
                "If the message was flagged as a violation, explain the issue politely. "
                "Otherwise, respond helpfully to their message. "
                "Do not be eager. Don't ask for followup. Just answer the question.\n\n"
                f"State: {state_summary}"
            )
        )
        result = await llm.ainvoke([system] + list(state["messages"]))
        return {"response": result.content}


    builder = StateGraph(BasicBotState)

    builder.add_node("moderation_check", moderation_check)
    builder.add_node("triage", triage)
    builder.add_node("analyze_question", questions_agent)
    builder.add_node("synthesize_response", synthesize_response)

    builder.add_edge(START, "moderation_check")
    builder.add_conditional_edges("moderation_check", route_moderation)
    builder.add_conditional_edges("triage", route_triage)
    builder.add_edge("analyze_question", "synthesize_response")
    builder.add_edge("synthesize_response", END)

    return builder.compile(checkpointer=checkpointer)