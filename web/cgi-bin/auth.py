#! /usr/bin/env python3

import cgi, cgitb
import os

import sys
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

form = cgi.FieldStorage()
form_login = form.getvalue('login')
form_password = form.getvalue('password')

if login.lower() == "root":
    password_correctness = os.system("%s%s/root-auth.sh %s" % (cfg.DIR_PATH['root'],
            cfg.DIR_PATH['scripts'], form_password))
    if password_correctness:
        password_is_correct = False
    else:
        password_is_correct = True

print(password_is_correct)
