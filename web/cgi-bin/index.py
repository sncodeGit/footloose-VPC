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
import html

if os.environ.get('REQUEST_URI') == "/":
    if db.is_users_exist():
        html.redirect_to('/auth')
    else:
        html.redirect_to('/install')
elif (os.environ.get('REQUEST_URI') == "/auth" and db.is_users_exist()):
    os.system(cfg.DIR_PATH['cgi-bin'] + 'auth.py')
elif (os.environ.get('REQUEST_URI') == "/install" and not db.is_users_exist()):
    os.system(cfg.DIR_PATH['cgi-bin'] + '/install.py')
elif (os.environ.get('REQUEST_URI') == "/create_root" and not db.is_users_exist()):
    form = cgi.FieldStorage()
    root_passw = form.getvalue('first_password')
    db.create_root(root_passw)
    html.redirect_to('/auth')
else:
    with open(cfg.DIR_PATH['error_pages'] + '/404.html', 'r') as file:
        html_404 = file.read()
    html.print_html()
    print(html_404)
