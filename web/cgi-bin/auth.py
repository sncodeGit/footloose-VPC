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
import htansw
import j2

template = 'auth.html.j2'
j2_vars = {
    'css_files': [cfg.URL_PATH['css'] + '/style.css',],
}
j2.print_j2_template(template, j2_vars)
