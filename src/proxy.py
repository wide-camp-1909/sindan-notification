import influxdb2
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'It works!')

    def do_POST(self):
        bytes = int(self.headers['Content-Length'])
        rawdata = self.rfile.read(bytes)
        jbody = json.loads(rawdata.decode('utf-8'))
        self.send_response(200)
        self.end_headers()


server = ThreadingHTTPServer(('0.0.0.0', 8081), RequestHandler)
server.serve_forever()