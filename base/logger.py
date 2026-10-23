import logging
from base.config import Config
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
log_file = project_root / Config.log_file
log_file.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger('mysql_query')
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
