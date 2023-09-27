import json
import time

import redis
from dotenv import dotenv_values


class Redis:
    def __init__(self, cfg_path='.env', time_out=1800, debug=False) -> None:
        config = dotenv_values(cfg_path)
        self.time_out = time_out
        self.debug = debug
        self.client = redis.StrictRedis(host='localhost',
                                        port=6379,
                                        db=0,
                                        password=config.get('REDIS', None))

    def update(self, uuid, data: str) -> None:
        assert 'time' in data, 'The stored data must contains a timestamp.'
        data = json.dumps(data)
        self.client.set(uuid, data)

    def fetch(self, uuid) -> str:
        data = self.client.get(uuid).decode('utf-8')
        data = json.loads(data)
        try:
            data['person'] = json.loads(data['person'])
        except TypeError:
            pass
        # skip expiration process when debugging
        if self.debug:
            return data
        assert 'time' in data, 'The stored data must contains a timestamp.'
        assert (time.perf_counter() - data['time']) <= self.time_out
        return data
