from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
from request import Request
from response import Response
from StaticResponder import StaticResponder
import views
from random import randint


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
            if '?' in request.uri:
                query_split = request.uri.split("?")
                request.uri = query_split[0]
                request.query = query_split[1]
            route_func = views.routes.get(request.uri, "404")
            if route_func == "404":
                response.set_status(Response.HTTP_NOT_FOUND)
            else:
                route_func(request, response)

        response.send()


class ThreadedTCPServe(ThreadingMixIn, TCPServer):
    pass


HOST, PORT = "127.0.0.1", 8001
TCPServer.allow_reuse_address = True

with TCPServer((HOST, PORT), HelloTCPServer) as s:
    print(f'Server on port: {PORT}')
    s.serve_forever()
