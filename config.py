import os

import pymysql
from pymysql.cursors import DictCursor

# En local usa los valores por defecto (root/root).
# En Railway, estas variables de entorno las provee automaticamente
# el plugin de MySQL, asi que no hay que tocar nada aqui.
DB_CONFIG = {
    "host": os.environ.get("MYSQLHOST", "localhost"),
    "user": os.environ.get("MYSQLUSER", "root"),
    "password": os.environ.get("MYSQLPASSWORD", "root"),
    "database": os.environ.get("MYSQLDATABASE", "mecanografia_db"),
    "port": int(os.environ.get("MYSQLPORT", 3306)),
    "cursorclass": DictCursor,
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)