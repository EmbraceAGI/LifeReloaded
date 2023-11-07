import json
import random
import re
import time
import uuid

from core import Chat, Database, Person
from prompts import BACKGROUND, EVAL, EVENTS, RULES


class Moderator:
    def __init__(self, expiration=1800, debug=False) -> None:
        self.redis = Database(time_out=expiration, debug=debug)
        self.chat = Chat(max_tokens=4000, debug=debug)
        self.expiration = expiration
        self.option_indicator = r'\n\d+\. '
        self.person = Person()

    def init_player(self, session_id):
        person = Person()
        data_dict = {'time': time.perf_counter(), 'person': str(person)}
        self.redis.update(session_id, data_dict)
        return json.loads(str(person))

    async def generate_background(self, session_id):
        data_dict = self.redis.fetch(session_id)

        chat_list = [RULES, BACKGROUND, ('user', str(data_dict['person']))]
        chat_stream = self.chat(chat_list)
        context = ''
        async for text in chat_stream:
            context += text
            yield text
        data_dict['background'] = context
        self.redis.update(session_id, data_dict)

    async def generate_events(self, session_id):
        data_dict = self.redis.fetch(session_id)

        chat_list = [
            RULES, EVENTS, ('user', data_dict['background']),
            ('user', str(data_dict['person'])),
            ('user', self.person.get_event_by_age(data_dict['person']['年龄']))
        ]
        chat_stream = self.chat(chat_list)
        context = ''
        async for text in chat_stream:
            context += text
            yield text
        event, option = self.parse_events(context)
        event_data = {'event': event, 'option': option}
        if 'events' in data_dict:
            data_dict['events'].append(event_data)
        else:
            data_dict['events'] = [event_data]
        self.redis.update(session_id, data_dict)

    async def evaluate_selection(self, session_id, selection: int):
        data_dict = self.redis.fetch(session_id)
        assert selection > 0 and selection <= 5

        chat_list = [
            RULES, EVAL, ('user', str(data_dict['person'])),
            ('user', data_dict['events'][-1]['event']),
            ('user', data_dict['events'][-1]['option']),
            ('user', str(selection))
        ]
        chat_stream = self.chat(chat_list)
        context = ''
        async for text in chat_stream:
            context += text
            yield text
        data_dict['events'][-1]['result'] = context

        # update age and personality
        added_age = random.randint(5, 10)
        data_dict['person']['年龄'] += added_age
        # TODO parse the 属性
        self.redis.update(session_id, data_dict)

    def parse_events(self, event: str):
        start = re.search(self.option_indicator, event).start() + 1
        event, options = event[:start], event[start:]
        return event, options

    def is_alive(self, session_id) -> bool:
        data_dict = self.redis.fetch(session_id)
        person = data_dict['person']
        if person['年龄'] >= 90:
            return False
        if person['属性']['健康'] <= 0:
            return False
        if person['属性']['幸福度'] <= 0:
            return False
        return True

    def get_parsed_event(self, session_id):
        data_dict = self.redis.fetch(session_id)
        event = data_dict['events'][-1]['event']
        option = data_dict['events'][-1]['option']
        return event, option

    def get_person_info(self, session_id):
        data_dict = self.redis.fetch(session_id)
        return data_dict['person']


if __name__ == '__main__':
    import asyncio

    async def iterate_stream(stream):
        async for _ in stream:
            continue

    moderator = Moderator(debug=True)

    session_id = str(uuid.uuid4())
    session_id = '5b845b00-a839-48f5-8e03-0f38e8cb16f6'
    print(session_id)

    moderator.init_player(session_id)
    asyncio.run(iterate_stream(moderator.generate_background(session_id)))

    while True:
        if not moderator.is_alive(session_id):
            break
        asyncio.run(iterate_stream(moderator.generate_events(session_id)))
        selection = input()
        asyncio.run(
            iterate_stream(
                moderator.evaluate_selection(session_id, int(selection))))
