import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from moderator import Moderator


class Item(BaseModel):
    message: str = None
    session_id: str = None
    selection: int = None


templates = Jinja2Templates(directory='templates')
moderator = Moderator(debug=False)
app = FastAPI()

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
app.mount('/life-reload/static',
          StaticFiles(directory='static'),
          name='static')


@app.get('/life-reload/', response_class=HTMLResponse)
async def game_root():
    return templates.TemplateResponse('game.html', {'request': {}})


@app.post('/life-reload/init/')
async def game_init(item: Item):
    session_id = item.session_id
    user_data = moderator.init_player(session_id)
    return user_data


@app.post('/life-reload/begin/')
async def game_begin(item: Item):
    session_id = item.session_id
    return StreamingResponse(moderator.generate_background(session_id),
                             media_type='text/plain')


@app.post('/life-reload/event/')
async def game_event(item: Item):
    session_id = item.session_id
    assert session_id is not None
    return StreamingResponse(moderator.generate_events(session_id),
                             media_type='text/plain')


@app.post('/life-reload/parsed_event/')
async def parsed_event(item: Item):
    session_id = item.session_id
    assert session_id is not None
    event, option = moderator.get_parsed_event(session_id)
    data = {'event': event, 'option': option}
    return data


@app.post('/life-reload/evaluation/')
async def evaluation(item: Item):
    session_id = item.session_id
    selection = item.selection
    assert session_id is not None and selection is not None
    return StreamingResponse(moderator.evaluate_selection(
        session_id, selection),
                             media_type='text/plain')


@app.post('/life-reload/is_alive/')
async def is_alive(item: Item):
    session_id = item.session_id
    assert session_id is not None
    return moderator.is_alive(session_id)


@app.post('/life-reload/get_person/')
async def get_person(item: Item):
    session_id = item.session_id
    assert session_id is not None
    return moderator.get_person_info(session_id)


if __name__ == '__main__':
    uvicorn.run('app:app',
                reload=True,
                port=5001,
                log_config='log_cfg.json',
                host='0.0.0.0',
                ssl_keyfile='./key.pem',
                ssl_certfile='./cert.pem')
