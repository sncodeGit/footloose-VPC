from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("188.68.219.27", 80)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()