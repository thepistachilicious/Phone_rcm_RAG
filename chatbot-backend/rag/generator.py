# rag/generator.py
from llama_index.core.query_engine import RetrieverQueryEngine
from rag.retriever import get_all_retrievers
from db.mongo import get_last_n_user_bot_messages
import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

from rag.retriever import get_all_retrievers  # nhập đúng theo project bạn

from rag.llm_utils import analyze_query_with_gemini  
import google.generativeai as genai


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)




# ✅ Hàm sinh phản hồi từ Gemini
def generate_gemini_response(query: str, context: str, history_context: str) -> str:
    full_prompt = f"""
    1. Dưới đây là đoạn hội thoại gần nhất giữa người dùng và trợ lý:
    {history_context}

    2. Kết hợp với ngữ cảnh từ tài liệu liên quan:
    {context}

    3. Câu hỏi hiện tại: {query}

    Kết hợp 3 mục trên và không tạo thông tin mới, tạo câu trả lời cho người dùng một cách tự nhiên, chính xác.
    Có thể rút gọn câu trả lời để đúng trọng tâm và phù hợp với câu hỏi nhất.
    """

    print("🤖 Gửi prompt tới Gemini thông qua LLM wrapper...")
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(full_prompt)
    return response.text.strip()

# ✅ Hàm chính gọi từ routes
async def get_llama_response(query: str) -> dict:
    print("🔍 Đang truy vấn tất cả retrievers...")

    try:
        context_lines = await get_last_n_user_bot_messages(n=3)
        history_context = "\n".join(context_lines)
    except Exception as e:
        print("⚠️ Không lấy được lịch sử:", e)
        history_context = ""
        
    analysis = analyze_query_with_gemini(query, history_context)
    
    if analysis.get("is_greeting") and analysis.get("answered"):
        return {
            "answer": analysis["answered"] or "Chào bạn! Tôi có thể giúp gì về điện thoại hoặc laptop?",
            "is_retrieved": False
        }

    if analysis.get("is_duplicate") and analysis.get("answered"):
        return {
            "answer": analysis["answered"],
            "is_retrieved": False
        }

    if analysis.get("is_ambiguous")  and analysis.get("new_query"):
        query = analysis["new_query"]

    target_name = analysis.get("retrieval_target", "").strip()



    retriever_tuples = get_all_retrievers()
    best_response = None
    best_retriever_name = None
    best_score = -1

    prioritized = []
    fallback = []
    for retriever_name, retriever in retriever_tuples:
        if target_name and target_name.lower() in retriever_name.lower():
            prioritized.append((retriever_name, retriever))
        else:
            fallback.append((retriever_name, retriever))

    all_retrievers = prioritized + fallback

    for retriever_name, retriever in prioritized:
        print(f"🔎 Đang truy vấn trong: {retriever_name}")

        query_engine = RetrieverQueryEngine.from_args(
            retriever=retriever,
            node_postprocessors=[
                SimilarityPostprocessor(similarity_cutoff=0.7)
            ],
        )

        try:
            response = query_engine.query(query)
        except Exception as e:
            print(f"❌ Lỗi khi truy vấn {retriever_name}:", e)
            continue

        if not response.source_nodes:  # <--- kiểm tra trước
            print(f"⚠️ {retriever_name} không trả về kết quả.")
            continue

        score = sum([node.score or 0 for node in response.source_nodes])  # an toàn rồi

        if score > best_score:
            best_response = response
            best_score = score
            best_retriever_name = retriever_name


    if not best_response or best_score == 0:
        return {
            "answer": "Không tìm thấy nội dung phù hợp.",
            "is_retrieved": False
        }

    context = "\n".join([node.node.get_content() for node in best_response.source_nodes])
    print(f"Sử dụng retriver trên tài liệu {best_retriever_name}")
    
    try:
        answer = generate_gemini_response(query, context, history_context)
    except Exception as e:
        print("🔥 Lỗi trong generate_gemini_response:", e)
        raise e

    return {
        "answer": answer,
        "retriever": best_retriever_name,
        "is_retrieved": True
    }

# nếu liên quan tới câu trên và không cần thông tin mới thì không cần đưa qua rag
