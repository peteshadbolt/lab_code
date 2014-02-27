import socket
from numpy import *

class client:
    def __init__(self):
        self.connected = 0
        self.sockobj = None
        self.debug=False
        self.connect()
        
    def connect(self):
        serverHost = 'localhost'
        serverPort = 50007
        print 'Initializing client...', 
        self.sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockobj.connect((serverHost, serverPort))
        self.connected = True
        print 'Done'

    def kill(self):
        print 'Closing client...'
        self.sockobj.close()    
        self.connected=False
    
    def say(self, command):
        self.sockobj.sendall(command)
        data = self.sockobj.recv(65536)
        return data

if __name__=='__main__':
    c=client()
    c.say('awd')
