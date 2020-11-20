#!/usr/bin/env python3

import subprocess
import sys
import cgi, cgitb
#
from jinja2 import Environment, FileSystemLoader

# Import config.py
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

# Import modules
sys.path.insert(0, cfg.DIR_PATH['modules'])
import db
import htansw
import auth_cookie

login = sys.argv[1]
passw = sys.argv[2]

try:
    if db.is_passw_correct(login, passw):
        auth_cookie.set_auth_session(auth_cookie.get_session_cookie())
    else:
        sys.exit(1)
except TypeError:
    sys.exit(2)
else:
    sys.exit(3)

