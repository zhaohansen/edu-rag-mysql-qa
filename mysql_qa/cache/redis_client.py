from base import Config, logger
import redis
import json
import pandas as pd


class RedisClient():
    def __init__(self):
        self.config = Config()
        self.logger = logger
        try:
            self.client = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                db=self.config.redis_db,
                password=self.config.redis_password,
                decode_responses=True
            )
            self.client.ping()
            self.logger.info("Redis 连接成功")
        except Exception as e:
            self.logger.error(f"Redis 连接失败：{e}")
            raise

    def set_data(self, key, value):
        try:
            self.client.set(key, json.dumps(value, ensure_ascii=False))
            self.logger.info("Redis 缓存写入成功")

        except Exception as e:
            self.logger.error(f"Redis 缓存写入失败：{e}")

    def get_data(self, key):
        try:
            result = self.client.get(key)
            if result:
                self.logger.info("Redis 缓存读取成功")
                return json.loads(result)
            else:
                self.logger.info("Redis 中未找到对应缓存数据")
                return None
        except redis.RedisError as e:
            self.logger.error(f"Redis 缓存读取失败：{e}")
            return None

    def get_answer(self, query):
        key = f"answer:{query}"
        return self.get_data(key)


if __name__ == "__main__":
    client = RedisClient()


