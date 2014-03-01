import socket
import sys
from multiprocessing import Process, Pipe
import time
import qy.settings
from easy_dpc import easy_dpc
import msvcrt


def postprocessing_loop(pipe):
	from postprocessing_server import postprocessing_server
	s=postprocessing_server(pipe)
	s.mainloop()


class dpc230_counting_server:        
    def __init__(self):
        ''' 
        This server continously acquires counts from the DPC230,
        and serves them over TCP/IP
        '''
        self.port=9999


    def dpc_callback(self, message):        
        ''' Gets called periodically during dpc.count_once '''
        print message
        return True


    def start(self):
        ''' Start up the server '''
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', self.port))

        # Start up the postprocessing sub-process
        self.pipe_tx, pipe_rx = Pipe()
        self.postprocessing = Process(target=postprocessing_loop, name='postprocessing_server', args=(pipe_rx,))
        self.postprocessing.start()

        # Wait for a connection
        self.connection_loop()

        print 'Shutting down server...'


    def connection_loop(self):
        ''' An infinite loop, connecting and disconnecting clients '''
        self.sock.listen(1)
        print 'Listening for connections on %d ...' % self.port
        while not msvcrt.kbhit():
            self.connection, self.client_address = self.sock.accept()
            print 'Connected to client %s, %s' % self.client_address
            self.dpc=easy_dpc(callback=self.dpc_callback)
            self.session_loop()
            print 'Lost connection with %s, %s' % self.client_address
            self.connection.close()
            self.dpc.kill()


    def session_loop(self):
        ''' Get commands from a connected client '''
        while True:
            try:
                message = self.connection.recv(4096)
                if not message: return
                print 'Recieved %s' % message
                self.handle_message(message)

            except socket.error:
                return


    def handle_message(self, message):
        ''' Handle a message from the client '''
        if message[0:3]=='int': 
            self.connection.sendall('HEEHEHE')
        else:
            self.connection.sendall(message.upper())


if __name__=='__main__':
    server=dpc230_counting_server()
    server.start()

