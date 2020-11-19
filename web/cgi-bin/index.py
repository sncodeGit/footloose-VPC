#!/usr/bin/env python3

import subprocess
import sys
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

# TODO Здесь же нужно возвращать ошибки!

html.print_html()
env = Environment(loader=FileSystemLoader('%s/' % cfg.DIR_PATH['templates']))
index_html = env.get_template('root_init.html.j2')
html_vars = {
    'css_files': [cfg.URL_PATH['css'] + '/style.css',],
    'js_files': [cfg.URL_PATH['js'] + '/root_init.js'],
}
output = index_html.render(html_vars=html_vars)
print(output)
