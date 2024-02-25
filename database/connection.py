from sqlite3 import connect as db_connect
from general.config import get_config

config = get_config()


def connect():
    return db_connect(config.DATABASE_URL)
