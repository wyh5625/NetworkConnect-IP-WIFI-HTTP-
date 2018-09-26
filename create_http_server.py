from http import server

server_address = ('', 44300)
httpd = server.HTTPServer(server_address, server.BaseHTTPRequestHandler)
httpd.serve_forever()