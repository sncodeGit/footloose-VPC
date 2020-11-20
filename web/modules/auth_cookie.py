import uuid
import http.cookies
import os
import sys

with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

def __get_session_cookie():
    return uuid.uuid4().hex

def __set_session(session_id):
    with open('%s/%s' % (cfg.DIR_PATH['tmp'], session_id), 'w') as f:
        f.write('0\n')

def set_auth_session(session_id):
    with open ('%s/%s' % (cfg.DIR_PATH['tmp'], session_id), 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('0', '1')
    with open ('%s/%s' % (cfg.DIR_PATH['tmp'], session_id), 'w') as f:
        f.write(new_data)

def get_session_cookie():
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    session_cookie = cookie.get("session_id")
    return session_cookie

def set_session_cookie():
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    session_cookie = cookie.get("session_id")
    if session_cookie is None:
        session_cookie = __get_session_cookie()
        __set_session(session_cookie)
        print("Set-cookie: session_id=%s" % session_cookie)
    return session_cookie

def is_user_auth(session_id):
    with open('%s/%s' % (cfg.DIR_PATH['tmp'], session_id)) as f:
        is_auth = f.read().split('\n')[0]
    if is_auth == 0:
        return False
    else:
        return True
