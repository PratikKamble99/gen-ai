from dotenv import load_dotenv
load_dotenv()
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

# with MongoDBSaver.from_conn_string(DB_URI) as checkpoint:
#     def call_model(state:State):
#         response = model.invoke(state.get("messages"))
#         return {"messages":[response]}

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

graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

# ADD CHECKPOINTER TO GRAPH
def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://root:password_123@localhost:27017/?authSource=admin"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpoint = compile_graph_with_checkpointer(checkpointer)

    # THIS CREATE THIS CHAT UNDER thread_id = pratik so we are persisting messages under same key
    config = {"configurable": {"thread_id": "pratik"}}

    # PASS YOUR CONFIG TO INVOKE GRAPH
    # updated_state = graph_with_checkpoint.invoke(State({"messages":["What is my name"]}), config=config)

    # GET RESPONSE IN STREAM
    for chunk in graph_with_checkpoint.stream(State({"messages":["What is my name"]}), config=config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()


    # print("UPDATED STATE",updated_state)



