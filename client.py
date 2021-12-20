import socket
from urllib.parse import urlparse

class Client(object):
    __AGENT = "HTTPTool/1.0"
    __TYPE = "application/x-www-form-urlencoded"
    __CRLF = '\r\n'
    def __init__(self, url):
        new_url, port, params = self.parse_url(url)
        url = urlparse(new_url)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = url.netloc
        self.path = url.path
        self.port = port
        self.params = params
        self.connect()

    def parse_url(self, url):
        try:
            index_init = int(url.index(':', 5)) + 1
            index_end = int(url.index('/', index_init))
            port = int(url[index_init:index_end])
        except:
            print("Default Port 80")
            port = 80
        url = url.replace(':' + str(port), '')
        try:
            index_init = int(url.index('?')) + 1
            params = url[index_init:]
            url = url.replace('?' + params, '')
        except:
            print("No params")
            params = ''
        return url, port, params


    def connect(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected at {self.host} port {self.port}s")

    def recv(self):
        data = b''
        part = None
        self.socket.settimeout(2)
        try:
            while part != b'':
                part = self.socket.recv(1024)
                data += part
        except socket.timeout:
            print('timeout')
        return data

    def GET(self):
        self.socket.send(('GET %s HTTP/1.1%sHost: %s%s' % (self.path, self.__CRLF, self.host, self.__CRLF + self.__CRLF)).encode())
        return self.recv()

    def POST(self):
        self.socket.send(('POST %s HTTP/1.1%sHost: %s%sUser-Agent: %s%sContent-Type: %s%sContent-Length: %d%s%s' %
                         (self.path, self.__CRLF,
                          self.host, self.__CRLF, self.__AGENT, self.__CRLF, self.__TYPE, self.__CRLF, len(self.params),
                          self.__CRLF + self.__CRLF,
                          self.params)).endcode())

        return self.recv()

    def close(self):
        self.socket.shutdown(1)
        self.socket.close()