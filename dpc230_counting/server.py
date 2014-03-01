import socket
import sys
from multiprocessing import Process, Pipe
import time
from qy.hardware import dpc230
import qy.settings
import msvcrt


def postprocessing_loop(pipe):
	from postprocessing_server import postprocessing_server
	s=postprocessing_server(pipe)
	s.mainloop()


class dpc_easy:
    ''' Talk to the DPC230 with less overhead '''
    def __init__(self, callback):
        ''' Set up defaults '''
        self.integration_time=1
        self.photon_buffer_switch=0
        self.photon_buffer_1=qy.settings.get('photon_buffer_1')
        self.photon_buffer_2=qy.settings.get('photon_buffer_2')
        self.dpc230=dpc230.dpc_daq(callback=callback)
        self.dpc230.print_setup_summary()


    def count_once(self):
        ''' The machine counts photons for one integration time '''
        # Choose a buffer
        which_buffer=self.photon_buffer_2 if self.photon_buffer_switch else self.photon_buffer_1
        self.photon_buffer_switch = not self.photon_buffer_switch
        tdc1, tdc2 = self.dpc230.count(which_buffer, self.integration_time)
        return tdc1, tdc2


    def kill(self):
        ''' Close connection '''
        self.dpc230.kill()
    

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
            self.dpc=dpc_easy(callback=self.dpc_callback)
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
                self.connection.sendall(message)
            except socket.error:
                return


if __name__=='__main__':
    server=dpc230_counting_server()
    server.start()

