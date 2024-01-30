#import http.server
#import ssl

#server_address = ('0.0.0.0', 8000)
#httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Use the generated SSL certificate
#httpd.socket = ssl.wrap_socket(httpd.socket, keyfile="/home/alpha/DigiYatra/server.key", certfile="/home/alpha/DigiYatra/server.cert", server_side=True)

#print(f"Serving on https://{server_address[0]}:{server_address[1]}")
#httpd.serve_forever()
import http.server
import ssl
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # If the root is requested, return the path to index.html
        if path == '/':
            return '/home/alpha/DigiYatra/index.html'
        # Otherwise, use the default handling to support other files
        return super().translate_path(path)

server_address = ('0.0.0.0', 8000)
httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)

# Use the generated SSL certificate
httpd.socket = ssl.wrap_socket(httpd.socket, keyfile="/home/alpha/DigiYatra/server.key", certfile="/home/alpha/DigiYatra/server.cert", server_side=True)

print(f"Serving on https://{server_address[0]}:{server_address[1]}")
httpd.serve_forever()
