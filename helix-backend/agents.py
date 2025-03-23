from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings, OpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, END, START, StateGraph
from langgraph.graph.message import add_messages
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from database import connection, cursor
import requests
from sql import INSERT_INTO_SEQUENCE_TABLE, UPDADATE_INTO_SEQUENCE_TABLE, GET_SEQUENCE_DATA

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

memory = MemorySaver()

sequence_id = 0

openai_model = ChatOpenAI(model="gpt-4o", api_key=openai_api_key, temperature=0.5)

@tool
def generate_sequence(num_steps: int, description: list, title: str):
    """
    This function allow chat agent to pass the information from user and generate sequence.
    Save to the database as well.

    Args:
        num_steps: int (number of steps)
        description: list (array of specific steps)
        title: str  (title)
    """
    try:
        cursor.execute(INSERT_INTO_SEQUENCE_TABLE, (title, num_steps, description))
        sequence_id = cursor.fetchone()[0]
        print("This is the id of recent sequence", sequence_id)
        
        connection.commit()

        print("Sequence add ok")
        return "Sequence done adding"
    except Exception as e:
        print(e)
        return e
    
@tool
def update_sequence(title: str, num_steps: int, description: list):
    """This is for update the sequence data directly by AI and request by user
    Maybe add more steps, change title

    Args:
        num_steps: int (number of steps)
        description: list (array of specific steps)
        title: str  (title)
    """

    print("Begin update state...")
    try:
        cursor.execute(UPDADATE_INTO_SEQUENCE_TABLE, (title, num_steps, description, "8"))
        print("Sequence update ok")
        connection.commit()

        return "Sequence done adding"
    except Exception as e:
        print(e)
        return e
    
class State(TypedDict):
    messages: Annotated[list, add_messages]

workflow = StateGraph(State)

tools = [generate_sequence, update_sequence]
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

workflow.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=[generate_sequence, update_sequence])
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges("chatbot", tools_condition)

workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

workflow_graph = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}


# user_input = "Write a HR sequence targeting candidates in software engineer involve email, offer letter, and interview"


# events = workflow_graph.stream(
#     {
#         "messages": [{"role": "user", "content": user_input}]
#     },
#     config=config,
#     stream_mode="values"
# )

# for event in events:
#     event["messages"][-1].pretty_print()







