# 📱 Chatbot Web Application

Dự án gồm 2 phần chính:

- **Frontend (Client):** Giao diện người dùng bằng React  
- **Backend (chatbot-backend):** API FastAPI xử lý chatbot, kết nối Gemini, Weaviate và MongoDB

---

## 🚀 Hướng dẫn cài đặt & chạy dự án

###
1️⃣ Frontend (Client)

```bash
cd client
npm i 
npm start
```
Truy cập giao diện web tại: http://localhost:3000
###
2️⃣ Backend (chatbot-backend)

- Bước 1: Cài đặt dependencies
```bash
cd chatbot-backend
pip install -r app/requirements.txt
```

- Bước 2: Cấu hình biến môi trường
Tạo file .env trong thư mục chatbot-backend với nội dung:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
CLUSTER_URL=your_weaviate_cluster_url_here
WEAVIATE_API_KEY=your_weaviate_api_key_here
MONGO_URI=your_mongodb_connection_string_here
```


- Bước 3: Cấu hình MongoDB trong file app/database/mongo.py (tạo database và collection trên mongodb)
```bash
db = client["chat"]            # Tên database MongoDB
message_collection = db["messages1"]  # Tên collection lưu trữ tin nhắn
```

- Bước 4: Khởi chạy backend
```bash
uvicorn app.main:app --reload --port 8000
```
