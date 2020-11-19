import pymysql
import sys

# Import config.py
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

def __mysql_connect(db):
    return pymysql.connect(db['host'], db['user'],
                            db['password'], db['name'])

def is_users_exist():
    db = __mysql_connect(cfg.DB)
    cursor = db.cursor()
    cursor.execute("CHECK TABLE users")
    db_answ = cursor.fetchone()
    if db_answ[3] == "Error":
        return 1
    else:
        return 0
