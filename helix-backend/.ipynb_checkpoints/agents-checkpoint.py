from typing import Annotated, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END, START
from langgraph.types import Command
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def define_system_prompt(suffix: str) -> str:
    return (
        "You are helpful AI assistant, collaborating with other AI assistants"
        "Use provided tools to answer and ask follow up questions."
        f"\n{suffix}"
        )


openai_model = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")

def get_next_node(last_message: AIMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return goto

# Chat agent and gather information
chat_agent = create_react_agent(openai_model, tools=[], prompt=define_system_prompt(""
"You can only do HR related tasks such as outreach, and ask follow up questions as needed identify sequence content. When "
"the information is enough, you begin to think about sequence, number of steps. You will be using that to work with sequence generator agents"""))

# Define the logic in chat_agent
def chat_agent_node(state: MessagesState) -> Command[Literal["sequence_generator", END]]:
    result = chat_agent.stream(state)
    goto = get_next_node(result["message"][-1], "sequence_generator")

    result["messages"][-1] = HumanMessage(content=result["messages"][-1].content, name="chat_agent")
    return Command(update={"messages": result["messages"]}, goto=goto)


# Sequence generator agent
sequences_agent = create_react_agent(openai_model, tools=[], 
                                     prompt=define_system_prompt("""
    You can only generate sequences of step with information on it. You are working with chat agent colleague
"""))


def sequence_agent_node(state: MessagesState) -> Command[Literal["chat_agent"]]:
    result = sequences_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "chat_agent")
    result["messages"][-1] = HumanMessage(content=result["messages"][-1].content, name="sequence_generator")
    return Command(update={"messages": result["messages"]}, goto=goto)

