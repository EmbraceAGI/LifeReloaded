import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chat_bot import chat, stream_chat, context
import time


class Item(BaseModel):
    message: str
    
templates = Jinja2Templates(directory="templates")

app = FastAPI(redoc_url="/chat/docs")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify the exact domain names, e.g., ["https://your-frontend-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/chat/static", StaticFiles(directory="static"), name="static")

@app.get("/chat/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/chat/send/")
async def send_message(item: Item):
    answer = await chat(context, item.message)
    return {"message_received": str(answer)}

@app.get("/chat/stream_chat/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index_stream.html", {"request": {}})


def word_stream():
    words = ["hello", "world", "from", "fastapi"]
    for word in words:
        yield word + " "  # 可以在每个单词后加空格或其他分隔符
        time.sleep(5)  # 模拟每秒发送一个单词
        
@app.post("/chat/stream_chat/send/")
def send_stream_message():
    # stream_chat(context, item.message)
    return StreamingResponse(word_stream(), media_type="text/plain")


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        reload=True,
        port=5001,
        host="0.0.0.0",
        ssl_keyfile="./key.pem",
        ssl_certfile="./cert.pem"
    )