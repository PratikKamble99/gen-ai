from dotenv import load_dotenv
load_dotenv()

from mem0 import Memory
from openai import OpenAI
import json
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

config = {
    "version":"v1.1",
    "embedder":{
        "provider":"openai",
        "config":{
            "api_key":OPENAI_API_KEY, "model":"text-embedding-3-small"
        }
    },
    "llm":{
        "provider": "openai",
        "config":{
            "api_key":OPENAI_API_KEY, "model":"gpt-4.1"
        }
    },
    "vector_store":{
        "provider":"qdrant",
        "config": {
            "host":"localhost",
            "port":6333
        }
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{
            "url":"neo4j+s://ef98ae2e.databases.neo4j.io",
            "username":"neo4j",
            "password":"wCu954ftcovEeFLiC20sU2kcZP21yd_k18tamhK1l4M",
        }
    }
}

mem_client = Memory.from_config(config)

while True:
        
    user_query = input("ASK: ")

    # THIS WILL FIND ONLY RELEVANT MEMORY
    search_memory = mem_client.search(user_id="pratik", query=user_query)

    memories = [
        f"ID: {memory.get("id")}\nMemory: {memory.get("memory")}" for memory in search_memory.get("results")
    ]

    SYSTEM_PROMPT = f""" 
        Here is the context about the user
        Context: {json.dumps(memories)}
     """
    
    print("FOUND MEMORIES: ",memories)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system", "content": SYSTEM_PROMPT},
            {"role":"user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message
    print("AI: ", ai_response)

    # This add automatic as factual, episodic and semantic memory
    mem_client.add(
        user_id="pratik",
        messages=[
            {"role":"user", "content": user_query},
            {"role":"assistant", "content":ai_response}
        ]
    )

    print("Memory has been sync")