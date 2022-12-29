from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url: urllib.parse.ParseResult = urllib.parse.urlparse(self.path)
        match pr_url.path:
            case pr_url.path "/":
                self.send_html_file('index.html')
            case pr_url.path "/contact":
                self.send_html_file('contact.html')

        
    def send_html_file(self, filename: str, status: int =200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
            
def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_adress: tuple = ('0.0.0.0', 8000)
    http: HTTPServer = server_class(server_adress, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
    
if __name__ == '__main__':
    run()