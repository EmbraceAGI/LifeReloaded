import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from chat_bot import context, stream_chat
from moderator import Moderator


class Item(BaseModel):
    message: str


templates = Jinja2Templates(directory='templates')
moderator = Moderator(debug=True)
app = FastAPI(redoc_url='/chat/docs')

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    # You can also specify the exact domain names, e.g.,
    # ["https://your-frontend-domain.com"]
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.mount('/chat/static', StaticFiles(directory='static'), name='static')
app.mount('/life-reload/static',
          StaticFiles(directory='static'),
          name='static')


@app.get('/chat/', response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse('index.html', {'request': {}})


@app.post('/chat/send/')
def send_stream_message(item: Item):
    return StreamingResponse(stream_chat(context, item.message),
                             media_type='text/plain')


@app.get('/life-reload/', response_class=HTMLResponse)
async def game_root():
    return templates.TemplateResponse('game.html', {'request': {}})


@app.get('/life-reload/init/')
async def game_init(request: Request):
    session_id = request.headers.get('session_id')
    user_data = moderator.init_player(session_id)
    return user_data


@app.get('/life-reload/begin/')
async def game_begin(request: Request):
    session_id = request.headers.get('session_id')
    return StreamingResponse(moderator.generate_background(session_id),
                             media_type='text/plain')


if __name__ == '__main__':
    uvicorn.run('app:app',
                reload=True,
                port=5001,
                host='0.0.0.0',
                ssl_keyfile='./key.pem',
                ssl_certfile='./cert.pem')
