#import socket
import SocketServer
import sys

class tcp_handler(SocketServer.BaseRequestHandler):        
    def __init__(self):
        ''' 
        This server continously acquires counts from the DPC230,
        and serves them over TCP/IP
        '''
        self.port=50007


    def start(self):
        ''' Start up the server '''
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))

        # Wait for a connection
        self.sock.listen(1)
        print 'Listening for connections on %d ...' % self.port
        while True:
            self.connection, self.client_address = self.sock.accept()
            print 'Connected to client %s, %s' % self.client_address
            self.mainloop()
            self.connection.close()


    def mainloop(self):
        ''' The main listening loop '''
        while True:
            message = self.connection.recv(1)
            if message:
                print 'Recieved %s' % message
                print 'Sending response to the client'
                self.connection.sendall(message)
            else:
                print 'Waiting..'


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

if __name__=='__main__':
    server=dpc230_counting_server()
    server.start()

