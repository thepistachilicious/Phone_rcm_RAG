from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)

db = client["chat"]  # tên database
message_collection = db["messages2"]  # tên collection

async def check_mongo_connection():
    """
    Hàm này cố gắng ping server MongoDB để kiểm tra kết nối.
    Nếu thành công, nó in ra thông báo thành công.
    Nếu không, nó in ra thông báo lỗi.
    """
    try:
        await client.admin.command('ping')
        print("✅ Đã kết nối thành công đến MongoDB!")
        return True
    except Exception as e:
        print(f"❌ Không thể kết nối đến MongoDB: {e}")
        return False

async def get_last_n_user_bot_messages(n=3) -> list[str]:
    cursor = message_collection.find().sort("timestamp", -1).limit(n * 2)  # USER-BOT pairs
    docs = await cursor.to_list(length=n * 2)
    docs.reverse()  # đảo ngược: từ cũ -> mới

    context_lines = []
    for msg in docs:
        prefix = "Người dùng" if msg["sender"] == "USER" else "Bot"
        context_lines.append(f"{prefix}: {msg['message']}")
    return context_lines
