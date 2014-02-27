#import socket
import sys
import SocketServer, socket


class counting_system_tcp_handler(SocketServer.StreamRequestHandler):        
    def handle(self):
        self.data = self.rfile.readline().strip()
        print '%s wrote %s' % (self.client_address[0], self.data)
        self.request.sendall(self.data.upper())
        self.request.close()

class counting_system_server(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

if __name__ == "__main__":
    HOST, PORT = 'localhost', 9999
    server = counting_system_server((HOST, PORT), counting_system_tcp_handler)
    server.serve_forever()


