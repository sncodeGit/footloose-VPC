#!/usr/bin/env python3

import pymysql

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
  <link rel="stylesheet" href="%s/style.css" media="screen" type="text/css" />
</head>
<body>
    <div id="login">
        <form method="post" action="index.html">
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
""" % cfg.DIR_PATH['css']

# TODO сделать with
db = pymysql.connect("localhost","flvpc","QVgMGF3VR3xw5Odt","flvpc_db" )
cursor = db.cursor()
cursor.execute("CHECK TABLE users")
db_answ = cursor.fetchone()

if db_answ[2] == "Error":
    print('Content-Type: text/html; charset=utf-8')
    print()
    print(initial_auth_page)