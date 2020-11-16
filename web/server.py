from http.server import HTTPServer, CGIHTTPRequestHandler

import os
config_path = os.system("cat /etc/footloose-vpc/footloose-vpc.conf")
path.insert(0, config_path)
import config as cfg

server_address = (cfg.LISTEN_IP, cfg.LISTEN_PORT)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
