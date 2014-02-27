import socket
import sys
from multiprocessing import Process, Pipe

def hardware_loop():
	from hardware_server import hardware_server
	s=hardware_server()
	s.mainloop()
	
def postprocessing_loop():
	from postprocessing_server import postprocessing_server
	s=postprocessing_server()
	s.mainloop()

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

        # Start up the hardware/postprocessing sub-processes
        hardware = Process(target=hardware_loop, name='hardware_server', args=())
        hardware.start()
        postprocessing = Process(target=postprocessing_loop, name='postprocessing_server', args=())
        postprocessing.start()

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

