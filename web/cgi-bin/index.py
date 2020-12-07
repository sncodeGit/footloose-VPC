#!/usr/bin/env python3

import subprocess
import sys
import os
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

# Get auth cookie
session_cookie = auth_cookie.set_session_cookie()

if os.environ.get('REQUEST_URI') == "/":
    if db.is_users_exist():
        htansw.redirect_to('/auth')
    else:
        htansw.redirect_to('/install')
elif (os.environ.get('REQUEST_URI') == "/auth" and db.is_users_exist()):
    os.system(cfg.DIR_PATH['cgi-bin'] + '/auth.py')
elif (os.environ.get('REQUEST_URI') == "/install" and not db.is_users_exist()):
    os.system(cfg.DIR_PATH['cgi-bin'] + '/install.py')
elif (os.environ.get('REQUEST_URI') == "/auth_me" and db.is_users_exist()):
    form = cgi.FieldStorage()
    form_passw = form.getvalue('password')
    form_login = form.getvalue('login')
    is_auth_process = subprocess.Popen([cfg.DIR_PATH['cgi-bin'] + '/auth_me.py', form_login, form_passw])
    is_auth = is_auth_process.wait()
    if not is_auth:
        htansw.redirect_to('/panel')
    else:
        htansw.redirect_to('/auth')
elif (os.environ.get('REQUEST_URI') == "/create_root" and not db.is_users_exist()):
    form = cgi.FieldStorage()
    root_passw = form.getvalue('first_password')
    db.create_root(root_passw)
    htansw.redirect_to('/auth')
else:
    with open(cfg.DIR_PATH['error_pages'] + '/404.html', 'r') as file:
        html_404 = file.read()
    htansw.print_html()
    print(html_404)
