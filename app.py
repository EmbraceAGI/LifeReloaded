import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chat_bot import chat, stream_chat, context


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
def send_stream_message(item: Item):
    return StreamingResponse(
        stream_chat(context, item.message), media_type="text/plain")
    
# TODO life-reload
# from main import Moderator
# moderator = Moderator()

# @app.get("/life-reload/", response_class=HTMLResponse)
# async def read_root():
#     return templates.TemplateResponse("index.html", {"request": {}})

# @app.post("/life-reload/send/")
# def send_stream_message(item: Item):
#     return StreamingResponse(
#         stream_chat(context, item.message), media_type="text/plain")

if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        reload=True,
        port=5001,
        host="0.0.0.0",
        ssl_keyfile="./key.pem",
        ssl_certfile="./cert.pem"
    )