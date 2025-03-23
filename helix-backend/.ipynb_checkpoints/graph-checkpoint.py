from langgraph.graph import StateGraph, START
from typing import Annotated, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END, START
from langgraph.types import Command
from agents import chat_agent_node, sequence_agent_node
from IPython.display import Image, display


def run_workflow():
    workflow = StateGraph(MessagesState)
    workflow.add_node("chat_agent", chat_agent_node)
    workflow.add_node("sequence_generator", sequence_agent_node)

    workflow.add_edge(START, "chat_agent")
    graph = workflow.compile()




    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
        graph.get_graph().draw_mermaid_png("workflow_graph.png")
    except Exception:
        # This requires some extra dependencies and is optional
        pass

run_workflow()