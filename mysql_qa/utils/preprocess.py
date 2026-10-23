import jieba
from base import logger


def preprocess_text(text):
    try:
        text = jieba.lcut(text)
        logger.info("文本分词完成")
        return text
    except Exception as e:
        logger.error(f"文本分词失败：{e}")
        return []

if __name__ == "__main__":
   text_content=preprocess_text("好吃,便宜实惠")
   print(text_content)

