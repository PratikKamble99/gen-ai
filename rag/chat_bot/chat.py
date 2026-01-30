from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

from dotenv import load_dotenv 

load_dotenv()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large",)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333/",
)

# Take user input
use_query = input("Ask something:  ")

# Relevant chunks from vector DB
search_result = vector_db.similarity_search(query=use_query)

context=[ "\n\n\n".join([f"Page Content: {result.page_content} \n Page Number: {result.metadata['page_label']} \n File location: {result.metadata["source"]}"]) for result in search_result]

SYSTEM_PROMPT=f""" 
    You are a helpful AI Assistant who answers user query based on the available context retrieved from PDF file along with page_number and page_contents.

    You should only ans the user questions based on following context and navigate the user to open the right page number to know more.

    Context:
    {context} 
 """
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.2",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {'role':"user", "content":use_query}
    ],
)

print(f"🤖: {response.choices[0].message.content} ")