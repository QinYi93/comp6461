import socket
import sys
from urllib.parse import urlparse
# from urllib.parse import urlencode
class http:

    def __init__(self, url):
        self.url = urlparse(url)
        self.host = self.url.netloc
        self.verbosity = False
        self.header = "\r\nHOST: " + self.host
    
    def send(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((self.host, 80))
            sys.stdout.write(self.content)
            conn.sendall(self.content.encode("utf-8"))
            response = conn.recv(1024, socket.MSG_WAITALL)
            return response.decode("utf-8")
        finally:
            conn.close()

    def setVerbosity(self, v):
        self.verbosity = v

    def getVerbosity(self):
        return self.verbosity

    def setHeader(self, header):
        self.header += header
        
    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setData(self, data):
        self.data = data

    def setFile(self, file):
        self.file = file

    def constructContent(self):
        path = self.url.path
        if path == "":
            path = "/"
        if self.url.query != "":
            query = "?"+self.url.query
        else:
            query = ""
    # construct get message
        if self.type == "get":
           self.content = self.type.upper() + " " + path + query + " HTTP/1.0" + self.header + "\r\n\r\n"

    # construct post message with data or file
        if self.type == "post":
            if self.data:
                self.content = self.type.upper() + " " + path + " HTTP/1.0" + self.header + "\r\n\r\n" + self.data
            if self.file:
                self.content = self.type.upper() + " " + path + " HTTP/1.0" + self.header + "\r\n\r\n" + self.file

