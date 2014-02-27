import socket
import sys

class client:
    def __init__(self):
        ''' An example client for the DPC230 server '''
        self.connect()

    def connect(self):
        serverHost = 'localhost'
        serverPort = 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((serverHost, serverPort))
        except socket.error:
            print 'Make sure that the DPC230 server is running!'
            sys.exit(0)

    def kill(self):
        self.sock.close()    

    def say(self, message):
        self.sock.sendall(message)
        response = self.sock.recv(65536)
        print 'Got %s back from the server' % response

if __name__=='__main__':
    c=client()
    try:
        while True:
            message=raw_input(' > ')
            c.say(message)
    finally:
        print 'Closing connections...'
        c.kill()


    
