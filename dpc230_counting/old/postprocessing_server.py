from time import sleep 
# TODO: should not print anywhere in here

class postprocessing_daemon:
    ''' 
    This code handles postprocessing and coincidence counting of timetags from the DPC230. 
    It runs as a daemon, belonging to the main TCP/IP server.
    '''
    def __init__(self, pipe ):
        ''' Gets a pipe to talk to the TCP/IP server '''
        self.pipe=pipe

    def mainloop(self):
        ''' Wait for messages to arrive over the pipe, and handle them '''
        print 'Postprocessor is awaiting commands.'
        while True:
            sleep(.01)
            while self.pipe.poll():
                message=self.pipe.recv()
                self.handle_message(message)

    def handle_message(self, message):
        ''' Handle a new message '''
        print 'Postprocessor recieved message "%s"' %  message
        if message=='shutdown': 
            print 'Postprocessor was shut down'
            return

