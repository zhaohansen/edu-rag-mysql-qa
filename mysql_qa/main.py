from db.mysql_client import MySQLClient
from cache.redis_client import RedisClient
from retrieval.bm25search import BM25Search
import time
from base import logger


class MySQLSystem():
    def __init__(self):
        self.bm25 = BM25Search()
        self.logger = logger

    def query(self, query):
        try:
            answer = self.bm25.search(query)
            if answer:
                self.logger.info("查询成功，已返回答案")
                return answer
            else:
                self.logger.info("MySQL 中未找到匹配答案")
                return None
        except Exception as e:
            self.logger.error(f"查询处理失败：{e}")
            return None


def main():
    system = MySQLSystem()
    print("欢迎使用 MySQL 智能问答系统")
    while True:
        query = input("请输入问题：")
        if query == "exit":
            print("系统关闭,感谢使用.")
            break
        else:
            answer = system.query(query)
            print("问题：", query)
            print("答案：", answer)


if __name__ == "__main__":
    main()
