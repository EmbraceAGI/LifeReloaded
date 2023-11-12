import json
import random
import re
import time
import uuid

from core import Chat, Database, Person
from prompts import BACKGROUND, EPITAPH, EVAL, EVENTS, RULES, SUM


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
        event_type = self.person.get_event_by_age(data_dict['person']['年龄'])
        chat_list = [
            RULES, EVENTS, ('user', data_dict['background']),
            ('user', str(data_dict['person'])), ('user', event_type)
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
        # format input
        selection = f'### 你的选择:\n**{selection}**'
        options = data_dict['events'][-1]['option']
        options = f'### 选项:\n{options}'
        person = str(data_dict['person'])
        person = f'### 你的基础信息：\n{person}'

        chat_list = [
            RULES, EVAL, ('user', data_dict['events'][-1]['event']),
            ('user', person), ('user', options), ('user', selection)
        ]
        chat_stream = self.chat(chat_list)
        context = ''
        async for text in chat_stream:
            context += text
            yield text
        data_dict['events'][-1]['result'] = context

        # summarize events
        sum_content = '\n'.join(
            [data_dict['events'][-1]['event'], options, selection, context])
        chat_list = [('user', SUM[1].format(sum_content))]
        chat_stream = self.chat(chat_list)
        sum_context = ''
        async for text in chat_stream:
            sum_context += text
        data_dict['events'][-1]['sum'] = sum_context

        # update age
        added_age = random.randint(5, 10)
        data_dict['person']['年龄'] += added_age
        # update attribute
        self.parse_eval(session_id, data_dict, context)

    async def generate_epitaph(self, session_id):
        data_dict = self.redis.fetch(session_id)
        pre_prompt = '### 你的历史事件(如果没有内容则表示当前还没有历史事件)\n***\n'
        if 'events' in data_dict:
            history = []
            for event in data_dict['events']:
                if 'sum' in event:
                    history.append(event['sum'])
                else:
                    continue
            history = '\n***\n'.join(history)
            history = pre_prompt + history
        else:
            history = pre_prompt
        chat_list = [EPITAPH, ('user', history)]
        chat_stream = self.chat(chat_list)
        context = ''
        async for text in chat_stream:
            context += text
            yield text

    def parse_events(self, event: str):
        start = re.search(self.option_indicator, event).start() + 1
        event, options = event[:start], event[start:]
        return event, options

    def parse_eval(self, session_id, data_dict: dict, results: str):
        begin_id = results.find('属性')
        results = results[begin_id:].replace("'", '')
        pattern = r'\s*(\w+):\s*(\d+)'
        matches = re.findall(pattern, results)
        if not matches:
            raise ValueError(f'mis pattern in: {results}')

        result_dict = {}
        for attribute, value in matches:
            value = int(value)
            value = 10 if value >= 10 else value
            value = 0 if value <= 0 else value
            result_dict[attribute] = value
        data_dict['person']['属性'] = result_dict
        # update person attribute
        self.redis.update(session_id, data_dict)

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
    session_id = '5b845b00-a839-48f5-8e03-0f38e8cb16f'
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
    asyncio.run(iterate_stream(moderator.generate_epitaph(session_id)))
