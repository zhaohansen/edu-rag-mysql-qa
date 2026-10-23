import numpy as np
from numpy import argmax
from base import logger
from mysql_qa.cache.redis_client import RedisClient
from mysql_qa.db.mysql_client import MySQLClient
from mysql_qa.utils.preprocess import preprocess_text
from rank_bm25 import BM25Okapi as BM25


class BM25Search:
    def __init__(self):
        self.logger = logger
        self.redis_client = RedisClient()
        self.mysql_client = MySQLClient()
        self.questions = None
        self.question_texts = None
        self.tokenized_questions = None
        self.bm25_model = None
        self.load_questions()

    def load_questions(self):
        original_key = "original_data"
        tokenizer_key = "tokenizer_data"

        self.question_texts = self.redis_client.get_data(original_key)
        self.tokenized_questions = self.redis_client.get_data(tokenizer_key)

        if self.question_texts and self.tokenized_questions:
            self.logger.info("问题库缓存命中")
            self.bm25_model = BM25(self.tokenized_questions)
            self.logger.info("BM25 检索模型初始化完成")
            return self.question_texts, self.tokenized_questions

        try:
            self.question_texts = self.mysql_client.fetch_questions()
            if self.question_texts:
                self.logger.info("已从 MySQL 加载问题库")
            else:
                self.logger.info("MySQL 中没有可用的问题数据")
                return [], []
        except Exception as e:
            self.logger.error(f"问题库加载失败：{e}")
            raise

        self.question_texts = [row[0] for row in self.question_texts]
        self.tokenized_questions = [preprocess_text(question) for question in self.question_texts]

        self.redis_client.set_data(original_key, self.question_texts)
        self.redis_client.set_data(tokenizer_key, self.tokenized_questions)
        self.logger.info("问题库已写入 Redis 缓存")
        self.bm25_model = BM25(self.tokenized_questions)
        self.logger.info("BM25 检索模型初始化完成")
        return self.question_texts, self.tokenized_questions

    def _softmax(self, scores):
        scores_exp = np.exp(scores - np.max(scores))
        return scores_exp / np.sum(scores_exp)

    def search(self, query, threshold=0.85):
        if not query or not isinstance(query, str):
            self.logger.error("问题不能为空，且必须是字符串")
            raise ValueError("query 必须是非空字符串")
        answer = self.redis_client.get_answer(query)
        if answer:
            self.logger.info("已从 Redis 缓存中获取答案")
            return answer
        try:
            tokenizer_question = preprocess_text(query)
            scores = self.bm25_model.get_scores(tokenizer_question)
            softmax_scores = self._softmax(scores)
            best_idx = argmax(softmax_scores)
            best_scores = softmax_scores[best_idx]
            best_text = self.question_texts[best_idx]

            print(f"最相似的问题：{best_text}")
            print(f"相似度：{best_scores}")

            if best_scores > threshold:
                answer = self.mysql_client.answer(best_text)
                if answer:
                    self.redis_client.set_data(f"answer:{query}", answer)
                    self.logger.info(f"答案匹配成功，相似度：{best_scores},答案已写入 Redis 缓存")
                    return answer
            else:
                self.logger.info(f"未找到可靠答案，最高相似度：{best_scores}<阈值：{threshold}")
                return None
        except Exception as e:
            self.logger.error(f"答案检索失败，数据库或检索模块异常：{e}")


if __name__ == "__main__":
    file = BM25Search()
    question_texts, tokenized_questions = file.load_questions()
    file.search("什么是Python的列表推导式")



