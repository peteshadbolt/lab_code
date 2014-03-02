import socket
import sys
import os
from multiprocessing import Process, Pipe
import time
import qy.settings
from easy_dpc import easy_dpc
import msvcrt
import logging
logging.basicConfig(filename='server.log', 
        level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

def postprocessing_loop(pipe):
	from postprocessing_daemon import postprocessing_daemon
	s=postprocessing_daemon(pipe)
	s.main_loop()


class dpc230_counting_server:        
    def __init__(self):
        ''' 
        This server continously acquires counts from the DPC230,
        and serves them over TCP/IP
        '''
        self.port=9999
        self.status_header=''
        self.show_status('Booting up...')


    def show_status(self, message=''):
        ''' Pretty-print the status to the screen '''
        #os.system('cls')
        #print 'DPC230 server'
        #print self.status_header
        print message
        #logging.info(self.status_header+' '+message)

    
    def dpc_callback(self, message):        
        ''' Gets called periodically during dpc.count_once '''
        self.show_status(message)
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

        # Handle connections
        self.main_loop()

        # Finally, shut down
        self.shutdown()

    def shutdown(self):
        ''' Try to shut down the server carefully '''
        self.show_status('Shutting down server ...')
        self.pipe_tx.send('shutdown')
        self.connection.close()
        self.dpc.kill()
        time.sleep(1)
        self.postprocessing.terminate()


    def main_loop(self):
        ''' An infinite loop, connecting and disconnecting clients '''
        self.dpc=easy_dpc(callback=self.dpc_callback)
        self.status_header=self.dpc.dpc230.get_setup_summary()
        self.show_status()
        self.sock.listen(1)
        self.show_status('Listening for connections on %d ...' % self.port)
        while True:
            self.connection, self.client_address = self.sock.accept()
            self.status_header = 'Connected to client %s, %s' % self.client_address
            self.show_status()
            self.session_loop()
            self.show_status('Lost connection with %s, %s' % self.client_address)
            self.connection.close()
        self.dpc.kill()

    def session_loop(self):
        ''' Get commands from a connected client '''
        while True:
            try:
                message = self.connection.recv(4096)
                if not message: return
                self.handle_message(message)

            except socket.error:
                return

    def integrate_once(self):
        ''' Integrate once, according to the current integration time '''
        tdc1, tdc2 = self.dpc.count_once()
        self.pipe_tx.send({'tdc1':tdc1, 'tdc2':tdc2})
        self.connection.sendall('HEEHEHE')
        self.show_status('Finished integrating')

    def handle_message(self, message):
        ''' Handle a message from the client '''
        if message == 'count': 
            self.integrate_once()
        elif message=='shutdown':
            self.shutdown()
            sys.exit(0)
        else:
            self.connection.sendall(message.upper())


if __name__=='__main__':
    server=dpc230_counting_server()
    server.start()

