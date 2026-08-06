import pymysql
from pymysql.cursors import DictCursor

# Ajusta estos datos segun tu instalacion de MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "mecanografia_db",
    "port": 3306,
    "cursorclass": DictCursor,
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)
