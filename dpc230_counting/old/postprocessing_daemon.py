from time import sleep 
#from qy.hardware.dpc230 import coincidence_counter
# TODO: should not print anywhere in here
from qy.hardware import dpc230
from qy.analysis import coincidence

class postprocessing_daemon:
    ''' 
    This code handles postprocessing and coincidence counting of timetags from the DPC230. 
    It runs as a daemon, belonging to the main TCP/IP server.
    '''
    def __init__(self, pipe):
        ''' Gets a pipe to talk to the TCP/IP server '''
        self.pipe=pipe
        self.dpc_post=dpc230('postprocessing')

    def main_loop(self):
        ''' Wait for messages to arrive over the pipe, and handle them '''
        while True:
            sleep(.01)
            if self.pipe == None: continue
            while self.pipe.poll():
                message=self.pipe.recv()
                self.handle_message(message)
                if message=='shutdown': return


    def handle_message(self, message):
        ''' Handle a new message '''
        #print 'Postprocessor recieved message "%s"' %  message
        if 'tdc1' in message: self.postprocess(message)


    def postprocess(self, message):
        ''' Postprocess some raw time-tag data '''
        # Read stuff from the message
        tdc1, tdc2 = message['tdc1'], message['tdc2']
                
        # Convert the raw data into meaningful timetags
        spc_filename = self.dpc_post.convert_raw_data(tdc1, tdc2)
        print spc_filename
            
        # count coincidences based on those timetags
        a=coincidence.process_spc(spc_filename)
        self.pipe.send(a)
            
if __name__=='__main__':
    p=postprocessing_daemon(None)
    p.main_loop()
