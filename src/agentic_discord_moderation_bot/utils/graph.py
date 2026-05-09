from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from agentic_discord_moderation_bot.utils.state import BasicBotState
from agentic_discord_moderation_bot.utils.model import ModerationFlag


# Functions
# moderation_check - flags messages that violate guidelines
# triage - determines which general workflow to follow (e.g. answer question, moderate, etc.)
# analyze_question - determines whether to answer a question directly or use tools
# analyze_moderation - determines which moderation actions to take, if any
# synthesize_response - generates a response to the user based on the current state


def create_graph(llm: BaseChatModel) -> CompiledStateGraph:
    """Build and compile the moderation graph with the given LLM.

    Parameters
    ----------
    llm : BaseChatModel
        The chat model to use in graph nodes.

    Returns
    -------
    CompiledStateGraph
        The compiled LangGraph ready for invocation.
    """
    moderation_llm = llm.with_structured_output(ModerationFlag)

    def moderation_check(state: BasicBotState) -> BasicBotState:
        message_content = state["message_ctx"].content
        system = SystemMessage(
            content=(
                "You are a Discord moderation assistant. "
                "Determine whether the following message violates community guidelines. "
                "Provide a structured output with the verdict, reason, and confidence score."
            )
        )
        result: ModerationFlag = moderation_llm.invoke([system, HumanMessage(content=message_content)])
        return {"moderation_flag": result}
    
    def triage(state: BasicBotState) -> dict:
        # TODO: determine which workflow to follow (answer question, use tools, etc.)
        return {}

    def route_moderation(state: BasicBotState) -> Literal["triage", "synthesize_response"]:
        flag: ModerationFlag = state["moderation_flag"]
        return "synthesize_response" if flag.verdict == "flagged" else "triage"


    def synthesize_response(state: BasicBotState) -> BasicBotState:
        system = SystemMessage(
            content=(
                "You are a Discord moderation assistant. "
                "Generate a concise, friendly reply to send to the user based on the context below. "
                "If the message was flagged as a violation, explain the issue politely. "
                "Otherwise, respond helpfully to their message."
            )
        )
        summary = (
            f"User message: {state['message_ctx'].content}\n"
            f"Moderation result: {state['moderation_flag'].model_dump()}"
        )
        result = llm.invoke([system, HumanMessage(content=summary)])
        return {"response": result.content}


    builder = StateGraph(BasicBotState)

    builder.add_node("moderation_check", moderation_check)
    builder.add_node("triage", triage)
    builder.add_node("synthesize_response", synthesize_response)

    builder.add_edge(START, "moderation_check")
    builder.add_conditional_edges("moderation_check", route_moderation)
    builder.add_edge("triage", "synthesize_response")
    builder.add_edge("synthesize_response", END)

    return builder.compile()