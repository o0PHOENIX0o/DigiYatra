
import http.server
import ssl
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # If the root is requested, return the path to index.html
        if path == '/':
            return 'DigiYatra/DigiYatra Rasp/Server/index.html'
        
        # Otherwise, use the default handling to support other files
        return super().translate_path(path)

server_address = ('0.0.0.0', 8000)
httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)

# Use the generated SSL certificate
httpd.socket = ssl.wrap_socket(httpd.socket, keyfile="DigiYatra/DigiYatra Rasp/Server/server.key", certfile="DigiYatra/DigiYatra Rasp/Server/server.cert", server_side=True)

print(f"Serving on https://{server_address[0]}:{server_address[1]}")
httpd.serve_forever()
