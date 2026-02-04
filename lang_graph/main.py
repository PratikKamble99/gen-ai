from dotenv import load_dotenv
load_dotenv()
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
model = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
    # temperature=0
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chat_bot(state: State):
    response = model.invoke(state.get("messages"))
    return {"messages":[response]}

def sample_node(state: State):
    return {"messages":["Sample message appended"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("sample_node", sample_node)

# CONNECT STARTING NODE
graph_builder.add_edge(START, "chat_bot")
# ADD WHICH NODE NEED TO RUN ANY STATE
graph_builder.add_edge("chat_bot", "sample_node")
graph_builder.add_edge("sample_node", END)

# COMPILE GRAPH
graph = graph_builder.compile()

# ADD INITIAL STATE INTO MESSAGES AND INVOKE GRAPH
updated_state = graph.invoke(State({"messages":["My name is Pratik"]}))

print("UPDATED STATE",updated_state)



