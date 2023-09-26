import asyncio
from typing import Any
import uuid
import time
import json

from prompts import RULES, BACKGROUND, EVENTS, EVAL
from core import Chat, Person, Redis


class Moderator:
    def __init__(self, expiration=1800) -> None:
        self.redis = Redis()
        self.chat = Chat(max_tokens=1500, debug=True)
        self.expiration = expiration
    
    def init_player(self, uuid):
        person = Person()
        data_dict = {
            'time': time.perf_counter(),
            'person': str(person)
        }
        self.redis.update(uuid, json.dumps(data_dict))

    def generate_background(self, uuid):
        data_dict = self.redis.fetch(uuid)
        data_dict = json.loads(data_dict)
        assert (time.perf_counter() - data_dict['time']) <= self.expiration
        
        chat_list = [RULES, BACKGROUND, ('user', data_dict['person'])]
        chat_flow = self.chat(chat_list)
        context = asyncio.run(self.chat.consume_chat(chat_flow))
        data_dict['background'] = context
        self.redis.update(uuid, json.dumps(data_dict))
        return chat_flow
    
    def generate_events(self, uuid):
        data_dict = self.redis.fetch(uuid)
        data_dict = json.loads(data_dict)
        assert (time.perf_counter() - data_dict['time']) <= self.expiration
        
        chat_list = [RULES, EVENTS, ('user', data_dict['background']), 
                     ('user', data_dict['person'])]
        chat_flow = self.chat(chat_list)
        context = asyncio.run(self.chat.consume_chat(chat_flow))
        if 'events' in data_dict:
            data_dict['events'].append(context)
        else:
            data_dict['events'] = [context]
        self.redis.update(uuid, json.dumps(data_dict))
        return chat_flow

    def evaluate_selection(self, uuid, selection: str):
        data_dict = self.redis.fetch(uuid)
        data_dict = json.loads(data_dict)
        # assert (time.perf_counter() - data_dict['time']) <= self.expiration
        
        chat_list = [RULES, EVAL, ('user', data_dict['person']),
                     ('user', data_dict['events'][-1]), ('user', selection)]
        chat_flow = self.chat(chat_list)
        context = asyncio.run(self.chat.consume_chat(chat_flow))
        # if 'events' in data_dict:
        #     data_dict['events'].append(context)
        # else:
        #     data_dict['events'] = [context]
        # self.redis.update(uuid, json.dumps(data_dict))
        return chat_flow

if __name__ == '__main__':
    moderator = Moderator()
    
    # session_id = str(uuid.uuid4())
    session_id = '5b845b00-a839-48f5-8e03-0f38e8cb16f6'
    print(session_id)
    
    # moderator.init_player(session_id)
    # moderator.generate_background(session_id)
    # moderator.generate_events(session_id)
    moderator.evaluate_selection(session_id, '5')
    stop = 1
