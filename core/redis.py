import redis
from dotenv import dotenv_values
import time


class Redis:
    def __init__(self, cfg_path='.env', time_out=1800) -> None:
        config = dotenv_values(cfg_path)
        self.time_out = time_out
        self.client = redis.StrictRedis(
            host='localhost', port=6379, db=0, 
            password=config.get('REDIS', None))

    def update(self, uuid, data: str) -> None:
        cur_time = time.perf_counter()
        self.client.set(uuid, data)

    def fetch(self, uuid) -> str:
        data = self.client.get(uuid)
        return data.decode("utf-8")
