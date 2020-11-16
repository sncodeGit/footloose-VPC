from http.server import HTTPServer, CGIHTTPRequestHandler

import os
import sys
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

server_address = (cfg.LISTEN_IP, cfg.LISTEN_PORT)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
