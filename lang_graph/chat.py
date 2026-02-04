from dotenv import load_dotenv
load_dotenv()
from typing import Annotated, Optional, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from openai import OpenAI

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print(f"chatbot node: {state.get('user_query')}")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user", "content":state.get("user_query")}
        ]
    )

    state['llm_output'] = response.choices[0].message
    return state

def evaluate_res(state:State) -> Literal['chatbot_gemini', "end_node"]:
    print(f"Evaluate node: {state.get('user_query')}")
    if False:
        return "end_node"
    
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print(f"chatbot gemini node: {state.get('user_query')}")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user", "content":state.get("user_query")}
        ]
    )

def end_node(state: State):
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("end_node", end_node)
graph_builder.add_node("evaluate_res", evaluate_res)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_res)

graph_builder.add_edge("chatbot_gemini", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query":"What is 2+2"}))
print(updated_state)