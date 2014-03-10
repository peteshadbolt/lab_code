import socket
import sys

# Create a TCP/IP socket
sock = socket.create_connection(('localhost', 10000))

try:
    # Send data
    message = 'This is the message.  It will be repeated.'
    sock.sendall(message)

    data = sock.recvline()
    print data

finally:
    sock.close()
