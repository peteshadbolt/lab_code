import socket

class client:
    def __init__(self):
        ''' An example client for the DPC230 server '''
        self.connect()


    def connect(self):
        serverHost = 'localhost'
        serverPort = 50007
        print 'Trying to connect to server on port %d ...' % serverPort, 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((serverHost, serverPort))
        print 'Done'


    def kill(self):
        print 'Closing client...'
        self.sock.close()    


    def say(self, message):
        print 'Sending %s' % message
        self.sock.sendall(message)
        response = self.sock.recv(65536)
        print 'Got %s back from the server' % response

if __name__=='__main__':
    c=client()
    while True:
        message=raw_input(' > ')
        c.say(message)
