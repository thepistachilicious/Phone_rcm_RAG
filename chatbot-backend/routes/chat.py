# routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.generator import get_llama_response  # ✅ Đúng hàm cần gọi
from db.mongo import message_collection
from db.message import Message as MessageModel

router = APIRouter()

class ChatQuery(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    is_retrieved: bool

@router.post("/api/chat/query", response_model=ChatResponse)
async def query_chatbot(query_data: ChatQuery):
    try:
        print(f"📥 Câu hỏi từ người dùng: {query_data.question}")

        # ✅ Gọi hàm async từ generator.py
        response = await get_llama_response(query_data.question)

        bot_response = response.get("answer", "Không tìm thấy câu trả lời phù hợp.")
        is_retrieved = response.get("is_retrieved", False)

        print("🤖 Phản hồi từ chatbot:", bot_response)
        print("📌 Truy vấn có tìm thấy context không:", is_retrieved)

        # Lưu tin nhắn người dùng
        user_message = MessageModel(sender="USER", message=query_data.question)
        await message_collection.insert_one(user_message.model_dump())

        # Lưu tin nhắn từ bot
        bot_message = MessageModel(sender="BOT", message=bot_response)
        await message_collection.insert_one(bot_message.model_dump())

        return ChatResponse(answer=bot_response, is_retrieved=is_retrieved)

    except Exception as e:
        print("🔥 Lỗi trong query_chatbot:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
