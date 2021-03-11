import os
import posixpath
import socket
import urllib
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from TabletControl.multithread_utilities import LoopThread


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Custom request handler used to host from specific path
    """
    def translate_path(self, path):
        """
        translates the path of where the server hosts from
        :param path: host path relative to project folder
        :return: translated path
        """
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

class RootedHTTPServer(HTTPServer):
    def __init__(self, base_path="host files/", port=8001, request_handler_class=RootedHTTPRequestHandler, print_root_address=True):
        """
        init
        :param base_path: relative path to host from
        :param port: server port
        :param request_handler_class: request handler to use
        :param print_root_address: prints the root address if set True
        """
        request_handler_class.base_path = base_path
        self.root_address = "http://" + self.get_ip() + ":" + str(port) + "/"
        server_adress = ("", port)
        HTTPServer.__init__(self, server_address=server_adress, RequestHandlerClass=request_handler_class)
        if print_root_address:
            print("Server address: " + self.root_address)

    def get_ip(self):
        """
        get the ip-address to the pc independent of the operating system
        :return: ip-address
        """
        return str(([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                  [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))

    def get_root_address(self):
        """
        gets the root folder address
        :return: root address
        """
        return self.root_address

    def handle_error(self, request, client_address):
        """Override handle error to avoid annoying prints of errors"""
        pass

class ServerThread(LoopThread):
    """server loop thread which you can stop, pause and resume"""
    def __init__(self, server):
        """
        init
        :param server: 
        """
        super(ServerThread, self).__init__(threadID=3, name="HTTP Server Thread")
        self.server = server

    def run_loop(self):
        """
        function to loop
        handles requests forever
        """
        try:
            self.server.handle_request()
        except Exception as e:
            pass