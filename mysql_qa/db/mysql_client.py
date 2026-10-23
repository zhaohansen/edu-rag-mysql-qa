from unittest import result

import pymysql
import pandas as pd
import sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
next_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(next_dir)
sys.path.insert(0, root_dir)

from base import Config, logger


class MySQLClient(object):
    def __init__(self):
        self.logger = logger
        try:
            self.conn = pymysql.connect(
                host=Config.mysql_host,
                user=Config.mysql_user,
                password=Config.mysql_password,
                db=Config.mysql_db,
            )
            self.cursor = self.conn.cursor()
            self.logger.info("MySQL 数据库连接成功")
        except pymysql.MySQLError as e:
            self.logger.error(f"MySQL 数据库连接失败：{e}")
            raise

    def create_table(self):

        sql_table = """
        CREATE TABLE IF NOT EXISTS jpkb(
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(100),
            question VARCHAR(1000),
            answer VARCHAR(1000)
            )
        """
        try:
            self.cursor.execute(sql_table)
            self.conn.commit()
            self.logger.info(f"数据表创建成功")
        except pymysql.MySQLError as e:
            self.logger.error(f"数据表创建失败：{e}")

    def insert_data(self):
        data = pd.read_csv("./jpkb_test_200.csv", encoding="utf8")
        try:
            for _, row in data.iterrows():
                insert_sql = "insert into jpkb(subject_name, question, answer) values(%s, %s, %s)"
                self.cursor.execute(insert_sql, (row["学科名称"], row["问题"], row["答案"]))
            self.conn.commit()
            self.logger.info("问答数据导入成功")
        except pymysql.MySQLError as e:
            self.conn.rollback()
            self.logger.error(f"问答数据导入失败：{e}")

    def fetch_questions(self):
        try:
            sql = "select question from jpkb "
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.logger.info(f"问题查询成功，匹配数量：{len(result)}")
            return result if result else None
        except pymysql.MySQLError as e:
            self.logger.error(f"问题查询失败：{e}")
            return None

    def answer(self, question):
        try:
            sql = "select answer from jpkb where question like %s"
            self.cursor.execute(sql, (f"%{question.strip()}%",))
            result = self.cursor.fetchall()
            self.logger.info(f"答案查询成功，匹配数量：{len(result)}")
            return result[0][0] if result else None
        except pymysql.MySQLError as e:
            self.logger.error(f"答案查询失败：{e}")
            return None

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            self.logger.info("MySQL 数据库连接已关闭")
        except  Exception as e:
            self.logger.error(f"MySQL 数据库连接关闭失败：{e}")

if __name__ == '__main__':
    mysql_client = MySQLClient()

    # mysql_client.create_table()
    # mysql_client.insert_data()

    question="什么是Python的列表推导式？"
    question_list=mysql_client.fetch_questions()
    print(f"问题列表：{question_list}")
    result = mysql_client.answer(question)
    if result:
        print(f"问题：{question}")
        print(f"答案：{result}")

    mysql_client.close()

