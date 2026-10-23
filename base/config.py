from configparser import ConfigParser
from pathlib import Path

config_file = Path(__file__).with_name('config.ini')
parser = ConfigParser()
parser.read(config_file, encoding='utf-8')


class Config:
    mysql_host = parser.get('mysql', 'host')
    mysql_user = parser.get('mysql', 'user')
    mysql_password = parser.get('mysql', 'password')
    mysql_db = parser.get('mysql', 'database')

    redis_host = parser.get('redis', 'host')
    redis_port = parser.get('redis', 'port')
    redis_password = parser.get('redis', 'password')
    redis_db = parser.get('redis', 'db')

    log_file = parser.get('logger', "log_file", fallback='logs/app.log')
