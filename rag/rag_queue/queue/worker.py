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
    # Relevant chunks from vector DB
)


def process_query(query:str):
    client = OpenAI()
    print("Searching query...")
    search_result = vector_db.similarity_search(query=query)

    context=[ "\n\n\n".join([f"Page Content: {result.page_content} \n Page Number: {result.metadata['page_label']} \n File location: {result.metadata["source"]}"]) for result in search_result]

    SYSTEM_PROMPT=f""" 
        You are a helpful AI Assistant who answers user query based on the available context retrieved from PDF file along with page_number and page_contents.

        You should only ans the user questions based on following context and navigate the user to open the right page number to know more.

        Context:
        {context} 
    """

    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role":"system", "content":SYSTEM_PROMPT},
            {'role':"user", "content":query}
        ],
    )

    return response
    

    # RUN CMD If worker not running on windows
    # rq worker --worker-class rq.worker.SimpleWorker
