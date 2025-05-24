# rag/retriever.py

from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.retrievers import VectorIndexRetriever

from weaviate.auth import AuthApiKey
import weaviate
import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from rag.custom_llm import OurLLM


load_dotenv()

weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
weaviate_url = os.getenv("CLUSTER_URL")

# define our LLM
Settings.llm = OurLLM()

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=AuthApiKey(weaviate_api_key),
)

embed_model = HuggingFaceEmbedding(model_name="hiieu/halong_embedding")

def build_index(index_name: str):
    vector_store = WeaviateVectorStore(
        weaviate_client=client,
        index_name=index_name,
        text_key="text"
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embed_model,
        llm=Settings.llm
    )
    return index

def build_retriever(index_name: str):
    index = build_index(index_name)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5  # Tăng top_k nếu muốn mở rộng tìm kiếm
    )
    return retriever

def get_all_retrievers():
    index_names = ["Phone_info", "Laptop_info", "QA"]
    return [(name, build_retriever(name)) for name in index_names]
