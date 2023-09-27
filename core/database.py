import json
import time

from dotenv import dotenv_values

try:
    from redis import StrictRedis as DatabaseBackend
except ImportError:
    # create a fake redis class
    class DatabaseBackend:
        def __init__(self, *args, **kwargs) -> None:
            self.data_base = {}

        def set(self, uuid: str, data: str):
            self.data_base[uuid] = data

        def get(self, uuid: str):
            return self.data_base[uuid]


class Database:
    def __init__(self, cfg_path='.env', time_out=1800, debug=False) -> None:
        config = dotenv_values(cfg_path)
        self.time_out = time_out
        self.debug = debug
        self.client = DatabaseBackend(host='localhost',
                                      port=6379,
                                      db=0,
                                      password=config.get('REDIS', None))

    def update(self, uuid, data: str) -> None:
        assert 'time' in data, 'The stored data must contains a timestamp.'
        data = json.dumps(data)
        self.client.set(uuid, data.encode('utf-8'))

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
