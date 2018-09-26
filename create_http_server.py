from http import server

server_address = ('', 8000)
httpd = server.HTTPServer(server_address, server.BaseHTTPRequestHandler)
httpd.serve_forever()