# routes/messages.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime
from db.mongo import message_collection
from db.message import Message as MessageModel

router = APIRouter()

class CreateMessage(BaseModel):
    sender: Literal["USER", "BOT"]
    message: str
    messageType: str = "text"

@router.post("/api/messages/", response_model=MessageModel)
async def create_message(message: CreateMessage):
    try:
        message_dict = message.model_dump()
        message_dict["timestamp"] = datetime.now()
        result = await message_collection.insert_one(message_dict)
        inserted_id = result.inserted_id  # Lấy ID đã chèn
        created_message = await message_collection.find_one({"_id": inserted_id})
        if created_message:
            return MessageModel(**created_message)
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve the newly created message from MongoDB") # lỗi chi tiết hơn
    except Exception as e:
        print(f"Error in create_message: {e}")  # In lỗi ra console
        raise HTTPException(status_code=500, detail=f"Failed to save message: {e}")  # Bao gồm cả lỗi gốc
    


@router.get("/api/messages/", response_model=List[MessageModel])
async def get_all_messages(limit: int = 100, skip: int = 0):
    messages = await message_collection.find().sort("timestamp", -1).skip(skip).limit(limit).to_list(None)
    return [MessageModel(**message) for message in messages]

@router.get("/api/messages/{message_id}", response_model=MessageModel)
async def get_message_by_id(message_id: str):
    message = await message_collection.find_one({"_id": message_id})
    if message:
        return MessageModel(**message)
    raise HTTPException(status_code=404, detail="Message not found")