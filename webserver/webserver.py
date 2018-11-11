#!/usr/bin/python

import SimpleHTTPServer
import SocketServer

class WebHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    # Disable logging DNS lookups
    def address_string(self):
        return str(self.client_address[0])


PORT = 8888
httpd = SocketServer.TCPServer(("", PORT), WebHandler)
print "Server: httpd serving at port", PORT
httpd.serve_forever()
