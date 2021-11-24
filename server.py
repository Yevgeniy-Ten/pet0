from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
from request import Request
from response import Response
from StaticResponder import StaticResponder


class HelloTCPServer(StreamRequestHandler):
    def handle(self):
        request = Request(self.rfile)
        response = Response(self.wfile)
        static_responder = StaticResponder(request, response, "static")

        if static_responder.file:
            response.set_status(response.HTTP_OK)
            static_responder.prepare_response()
        else:
            response.add_header("Content-Type", "text/html")
            response.add_header("Connection", "close")
            response.set_body('<h1>Hello, world!</h1>')

        response.send()


class ThreadedTCPServe(ThreadingMixIn, TCPServer):
    pass


HOST, PORT = "127.0.0.1", 8000
TCPServer.allow_reuse_address = True

with TCPServer((HOST, PORT), HelloTCPServer) as s:
    s.serve_forever()
