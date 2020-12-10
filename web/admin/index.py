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
import j2

# Get auth cookie
session_cookie = auth_cookie.set_session_cookie()
if not auth_cookie.is_user_auth(session_cookie):
    with open(cfg.DIR_PATH['error_pages'] + '/404.html', 'r') as file:
        html_404 = file.read()
    htansw.print_html()
    print(html_404)
#TODO
if not auth_cookie.is_user_admin(session_cookie):
    with open(cfg.DIR_PATH['error_pages'] + '/404.html', 'r') as file:
        html_404 = file.read()
    htansw.print_html()
    print(html_404)

if os.environ.get('REQUEST_URI') == "/admin":
    template = 'admin_index.html.j2'
    j2_vars = {}
    j2.print_j2_template(template, j2_vars)
if os.environ.get('REQUEST_URI') == "/admin/logout":
    htansw.redirect_to('/auth')