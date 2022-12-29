from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from threading import Thread
import mimetypes
import pathlib
import urllib.parse
import socket


UDP_IP = '127.0.0.1'
UDP_PORT = 5000
HTTP_PORT = 3000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url: urllib.parse.ParseResult = urllib.parse.urlparse(self.path)
        match pr_url.path:
            case "/":
                self.send_html_file('index.html')
            case "/message":
                self.send_html_file('message.html')
            case other:
                if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                    self.send_static()
                else:
                    self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        run_socket_client(UDP_IP, UDP_PORT, data=data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename: str, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as fd:
            self.wfile.write(fd.read())


def run_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_adress: tuple = ('0.0.0.0', HTTP_PORT)
    http: HTTPServer = server_class(server_adress, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server(ip: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        server = ip, port
        sock.bind(server)
        try:
            while True:
                data, address = sock.recvfrom(1024)
                print(f'Received data: {data.decode()} from: {address}')
                data_parse = urllib.parse.parse_qsl(data)
                result = json.dumps({(str(datetime.now())).decode(): dict(data_parse)})
                with open("./storage/data.json", "wb") as fd:
                    json.dump(result, fd)
                server.sendto(data, address)
        except KeyboardInterrupt:
            print("Destroy Server")


def run_socket_client(ip: str, port: int, data=None):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        server = ip, port
        client.sendto(data, server)
        response, address = client.recvfrom(1024)
        print(f'Response data: {response.decode()} from address: {address}')


HTTPServer = Thread(target=run_server)
UDPServer = Thread(target=run_socket_server, args=(UDP_IP, UDP_PORT))
UDPClient = Thread(target=run_socket_client, args=(UDP_IP, UDP_PORT))


if __name__ == '__main__':
    HTTPServer.start()
    UDPServer.start()
    UDPClient.start()
    HTTPServer.join()
    UDPServer.join()
    UDPClient.join()
