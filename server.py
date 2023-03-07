import urllib.parse
import pathlib
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = pathlib.Path()

class HTTPHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        lenght = self.headers.get('Content-Length')
        data = self.rfile.read(int(lenght))
        print(urllib.parse.unquote_plus(data.decode()))
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)

        match route.path:
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

                
    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read()) 

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mt = mimetypes.guess_type(filename)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read()) 

def run():
    address = ('localhost', 3000)
    http_server = HTTPServer(address, HTTPHandler)

    try: 
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

if __name__ == "__main__":
    run()