# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import messages, chat  # Import module chat

app = FastAPI()

origins = [
    "http://localhost:3000"
]

# CORS middleware để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép tất cả các origin (trong môi trường production nên giới hạn)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include các router
app.include_router(messages.router)
app.include_router(chat.router)  # Include router chat

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)