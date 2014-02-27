
class dpc230_counting_server:        
    def __init__(self):
        ''' 
        This server continously acquires counts from the DPC230,
        and serves them over TCP/IP
        '''


server=lab_server()
server.main_loop()

