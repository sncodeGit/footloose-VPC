#! /usr/bin/env python3

import cgi, cgitb
import os
import sqlite3

import sys
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

initial_auth_page = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Footloose-VPC</title>
  <link rel="stylesheet" href="%s%s/style.css" media="screen" type="text/css" />
</head>
<body>
    <div id="login">
        <form method="post" action="cgi-bin/auth.py">
            <fieldset class="clearfix">
                Пожалуйста, введите пароль root-пользователя
                <p><span class="fontawesome-user"></span><input name="login" type="text" value="login" onBlur="if(this.value == '') this.value = 'login'"        onFocus="if(this.value == 'login') this.value = ''" required></p> <!-- JS because of IE support; better: placeholder="Username" -->
                <p><span class="fontawesome-lock"></span><input name="password" type="password"  value="password" onBlur="if(this.value == '') this.value = 'password'" onFocus="if(this.value == 'password') this.value = ''" required></p> <!-- JS because of IE support; better: placeholder="Password" -->
                <p><input type="submit" value="Login"></p>
            </fieldset>
        </form>
    </div>
</body>
</html>
""" % (cfg.DIR_PATH['root'], cfg.DIR_PATH['css'])

form = cgi.FieldStorage()
form_login = form.getvalue('login')
form_password = form.getvalue('password')

conn = sqlite3.connect(r'%s/db.sqlite3' % cfg.DIR_PATH['db'])
cur = conn.cursor()
try:
    cur.execute("SELECT UserPass FROM Users WHERE UserName = root")
except sqlite3.OperationalError:
    # Вернуть страницу первоначальной настройки
    print(initial_auth)
finally:
    pass