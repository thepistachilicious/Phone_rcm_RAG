# # retriever.py

# import os
# import atexit
# import nest_asyncio
# import asyncio
# from dotenv import load_dotenv

# from llama_index.vector_stores.weaviate import WeaviateVectorStore
# from llama_index.core import VectorStoreIndex, StorageContext, Document
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.core.retrievers import QueryFusionRetriever
# from llama_index.retrievers.bm25 import BM25Retriever
# from llama_index.core.storage.docstore import SimpleDocumentStore
# from llama_index.core import Settings

# import weaviate
# from weaviate.auth import AuthApiKey
# from weaviate import WeaviateAsyncClient
# from weaviate.classes.init import AdditionalConfig

# # ✅ Cho phép nested async
# nest_asyncio.apply()

# # ✅ Load .env
# load_dotenv()
# weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
# weaviate_url = os.getenv("CLUSTER_URL")

# # ✅ Khởi tạo Async Client
# async_client =  weaviate.use_async_with_weaviate_cloud(
#     cluster_url=weaviate_url,
#     auth_credentials=AuthApiKey(weaviate_api_key),
#     additional_config=AdditionalConfig(timeout=(60, 60)), 
# )
# # ✅ Embedding
# embed_model = HuggingFaceEmbedding(model_name="hiieu/halong_embedding")
# Settings.llm = None  # bạn có thể gắn LLM nếu cần


# async def build_retriever(index_name: str):
#     # ✅ Khởi tạo vector store với async client
#     vector_store = WeaviateVectorStore(
#         weaviate_client=async_client,
#         index_name=index_name,
#         text_key="text",
#     )

#     storage_context = StorageContext.from_defaults(vector_store=vector_store)

#     # ✅ Lấy documents từ Weaviate
#     collection = async_client.collections.get(index_name)
#     results = await collection.query.fetch_objects(limit=100)
#     docs = []

#     for obj in results.objects:
#         if "text" in obj.properties and obj.properties["text"].strip():
#             docs.append(Document(text=obj.properties["text"]))

#     print(f"📦 Số lượng documents thực tế trong {index_name}:", len(docs))

#     # ✅ Tạo docstore từ documents
#     docstore = SimpleDocumentStore()
#     docstore.add_documents(docs)

#     storage_context.docstore = docstore

#     index = VectorStoreIndex.from_vector_store(
#         vector_store=vector_store,
#         storage_context=storage_context,
#         embed_model=embed_model,
#         llm=Settings.llm,
#     )
    
#     return index.as_retriever(similarity_top_k=3)

#     if len(docs) == 0:
#         print(f"⚠️ Không có tài liệu text trong {index_name}, bỏ qua BM25.")
#         return index.as_retriever(similarity_top_k=3)

#     # ✅ Kết hợp BM25 + vector retriever
#     vector_retriever = index.as_retriever(similarity_top_k=3)
#     bm25_retriever = BM25Retriever.from_defaults(
#         docstore=docstore,
#         similarity_top_k=3
#     )

#     fusion_retriever = QueryFusionRetriever(
#         [vector_retriever, bm25_retriever],
#         similarity_top_k=3,
#         num_queries=1,
#         mode="reciprocal_rerank",
#         use_async=True,
#         verbose=True
#     )

#     return fusion_retriever


# async def get_all_retrievers():
#     index_names = ["Phone_info", "Laptop_info", "QA"]
#     retrievers = []
    
#     if not async_client.is_connected():
#         await async_client.connect()

#     for name in index_names:
#         retriever = await build_retriever(name)
#         retrievers.append((name, retriever))

#     return retrievers


# # ✅ Cleanup async client on exit
# atexit.register(lambda: asyncio.run(async_client.close()))
