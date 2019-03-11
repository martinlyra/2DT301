from threading import Thread

from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from xml.etree import ElementTree


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, handler_class, master):
        self.master = master
        super().__init__(address, handler_class)


class WebServerConfig(object):
    def __init__(self, config_tree : ElementTree):
        self.port = int(config_tree.find('port').text)


class WebHttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.end_headers()
        self.send_response(200, "")

    def do_POST(self):
        pass


class HttpWebServer(Thread):
    httpHandler = SimpleHTTPRequestHandler
    httpSocket = None

    serverConfig = None

    def __init__(self, config_tree : ElementTree):
        super().__init__()
        self.serverConfig = WebServerConfig(config_tree)

        self.httpSocket = ThreadingHttpServer(("", self.serverConfig.port), self.httpHandler, self)

    def check_user(self):
        pass

    def run(self):
        self.httpSocket.serve_forever()

    def shutdown(self):
        self.httpSocket.shutdown()
