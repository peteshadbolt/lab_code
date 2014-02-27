import socket
import sys

class dpc230_counting_server:        
    def __init__(self):
        ''' 
        This server continously acquires counts from the DPC230,
        and serves them over TCP/IP
        '''
        self.port=9999

    def start(self):
        ''' Start up the server '''
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', self.port))

        # Wait for a connection
        self.sock.listen(1)
        print 'Listening for connections on %d ...' % self.port
        while True:
            self.connection, self.client_address = self.sock.accept()
            print 'Connected to client %s, %s' % self.client_address
            self.mainloop()
            print 'Lost connection with %s, %s' % self.client_address
            self.connection.close()

    def mainloop(self):
        ''' The main listening loop '''
        while True:
            message = self.connection.recv(4096)
            if message:
                print 'Recieved %s' % message
                self.connection.sendall(message)
            else:
                return

if __name__=='__main__':
    server=dpc230_counting_server()
    server.start()

