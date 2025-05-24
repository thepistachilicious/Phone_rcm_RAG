# models/message.py
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class Message(BaseModel):
    sender: Literal["USER", "BOT"]
    message: str
    messageType: str = "text"
    timestamp: datetime = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "sender": "USER",
                "message": "Xin chào!",
                "messageType": "text",
            }
        }