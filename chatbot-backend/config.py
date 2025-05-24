# chatbot-backend/config.py
import os
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
CLUSTER_URL = os.getenv("CLUSTER_URL")

# Optional: log lỗi nếu thiếu biến
if not WEAVIATE_API_KEY or not CLUSTER_URL:
    raise ValueError("Missing required environment variables in .env")
