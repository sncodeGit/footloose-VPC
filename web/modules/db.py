import pymysql
import sys

# Import config.py
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

import hash

def __mysql_connect(db):
    return pymysql.connect(host=db['host'], user=db['user'],
                            passwd=db['password'], db=db['name'],
                            autocommit=True)

def is_users_exist():
    db = __mysql_connect(cfg.DB)
    cursor = db.cursor()
    cursor.execute("CHECK TABLE users")
    db_answ = cursor.fetchone()
    if db_answ[2] == "Error":
        return False
    else:
        return True

def __create_users_table():
    db = __mysql_connect(cfg.DB)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE users(
        user_id INT NOT NULL AUTO_INCREMENT UNIQUE,
        user_name VARCHAR(20) NOT NULL UNIQUE,
        user_pass VARCHAR(100) NOT NULL,
        PRIMARY KEY ( user_id )
        );
    """)

def create_root(root_passw):
    if not is_users_exist():
        __create_users_table()

    db = __mysql_connect(cfg.DB)
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO `users` (`user_id`, `user_name`, `user_pass`)
    VALUES (default, 'root', '%s');
    """ % hash.hash_password(root_passw))

def is_passw_correct(login, passw):
    db = __mysql_connect(cfg.DB)
    cursor = db.cursor()
    cursor.execute("""
    SELECT user_pass FROM users WHERE user_name='%s';
    """ % login)
    db_passw_hash = cursor.fetchone()[0]
    return hash.check_password(db_passw_hash, passw)
