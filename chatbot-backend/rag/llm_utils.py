# rag/llm_utils.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)


def analyze_query_with_gemini(query: str, history_context: str) -> dict:
    prompt = f"""
    Lịch sử hội thoại:
    {history_context}

    Câu hỏi mới: "{query}"

    Phân tích:
    1. Câu hỏi có mơ hồ không và cần được làm rõ dựa trên lịch sử hội thoại không? (true/false)
    2. Câu hỏi đã được trả lời trước đó trong lịch sử chưa? (true/false)
    3. Nếu đã trả lời, trích xuất câu trả lời từ lịch sử.
    4. Nếu mơ hồ vì liên quan đến lịch sử, viết lại câu hỏi cho rõ ràng, không thêm thông tin mới.

    Trả lời theo định dạng JSON:
    {{
      "is_ambiguous": True/False,
      "is_duplicate": True/False,
      "answered": "nội dung câu trả lời hoặc rỗng",
      "clarified_query": "câu hỏi rõ ràng hoặc rỗng"
    }}
    """

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        # Loại bỏ dấu ```json và ```
        cleaned_response = re.sub(r"^```json|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()

        print("🎯 Phản hồi từ Gemini:", cleaned_response)  # Debug
        try:
            result = json.loads(cleaned_response)
        except json.JSONDecodeError as json_err:
            print("Lỗi phân tích JSON:", json_err)
            raise ValueError("Phản hồi không ở định dạng JSON hợp lệ.")

    except Exception as e:
        print("Lỗi khi phân tích phản hồi từ Gemini:", e)
        result = {
            "is_ambiguous": False,
            "is_duplicate": False,
            "answered": "",
            "clarified_query": query
        }
    return result

