#!/usr/bin/env python3

import subprocess
import sys

# Import config.py
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

# Здесь же нужно возвращать ошибки!

print('Content-Type: text/plain; charset=utf-8')
print()
print('Hello')
a = subprocess.Popen(['python3', 'test.py'])
print(a)