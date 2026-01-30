from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv 

load_dotenv()

file_path = Path(__file__).parent / "cg-internal-docs.pdf"

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)

# load file in python program
loader = PyPDFLoader(file_path)
docs = loader.load()

# Split the docs into smaller chunks
chunks = text_splitter.split_documents(docs)

# Create vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large",)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333/",
)

print("indexing of document done")