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

    Trả lời theo đúng định dạng JSON sau:
    {{
        "is_greeting": "True hoặc rỗng",
      "is_ambiguous": "True hoặc rỗng",
      "is_duplicate": "True hoặc rỗng",
      "answered": "nội dung câu trả lời hoặc rỗng",
      "new_query": "câu hỏi rõ ràng hoặc rỗng",
      "retrieval_target": "Phone_info/Laptop_info hoặc rỗng nếu không rõ"
    }}
    
    Phân tích:
    1. Nếu câu hỏi là lời chào xã giao (ví dụ: xin chào, bạn khỏe không, bạn là ai, cảm ơn nhé, tạm biệt, hẹn gặp lại...), không liên quan tới thông tin điện thoại hoặc laptop thì "is_greeting" là True.
    2. Nếu is_greeting là True thì mục "answered" nên là câu phản hồi lịch sự, ví dụ: "Chào bạn, tôi có thể giúp gì về điện thoại hoặc laptop?".
    4. Nếu câu hỏi mơ hồ (thường chứa các từ: nó, ấy, đó, kia, cái nào, như trên, đã đề cập,...) do phụ thuộc ngữ cảnh thì "is_ambiguous" là True.
    5. Nếu có thể viết lại câu hỏi rõ ràng hơn từ ngữ cảnh thì điền vào "new_query", còn không thì giữ nguyên, không được thêm thông tin mới.
    6. Nếu câu hỏi đã từng được hỏi và được trả lời trong lịch sử thì "is_duplicate" là True và "answered" là câu trả lời trích từ lịch sử; ngược lại "is_duplicate" là "" và "answered" là ""
    7. Truy vấn này liên quan đến chủ đề nào điện thoại hay laptop: "Phone_info", "Laptop_info", ""? (retrieval_target)
    """

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        cleaned_response = re.sub(r"^```json|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()

        print("🎯 Phản hồi từ Gemini:", cleaned_response)
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
            "new_query": query,
            "retrieval_target": ""
        }

    return result

