#! /usr/bin/env python3

import cgi, cgitb

import os
config_path = os.system("cat /etc/footloose-vpc/footloose-vpc.conf")
path.insert(0, config_path)
import config as cfg

form = cgi.FieldStorage()
form_login = form.getvalue('login')
form_password = form.getvalue('password')

if login.lower() == "root":
    pass_check = os.system("%s%s/root-auth.sh %s" % (cfg.DIR_PATH['root'],
            cfg.DIR_PATH['scripts'], form_password))
    if pass_check.lower() == "correct":
        password_is_correct = True
    else:
        password_is_correct = False

print(password_is_correct)
