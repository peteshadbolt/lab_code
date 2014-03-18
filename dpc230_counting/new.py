from multiprocessing import Process, Pipe 
import time, sys
import signal

class post:
    ''' The postprocessing process '''
    def __init__(self, pipe):
        # Create hook to SIGINT
        signal.signal(signal.SIGINT, self.shutdown)

        # Set up
        self.name='post'
        self.pipe=pipe
        #self.send_text_message('Booting up postprocessing...')

        # Start listening
        self.listen()

    def listen(self):
        ''' Keep on looping '''
        while True:
            time.sleep(.1)
            while self.pipe.poll():
                message=self.pipe.recv()
                self.handle_message(message)

    def handle_message(self, message):
        ''' Handle a message coming from the client ''' 
        if message[0]=='tdc': 
            self.handle_tdc(message)
        elif message[0]=='shutdown': 
            self.shutdown()
        elif message[0]=='delays': 
            self.set_delays(message[1])


    def set_delays(self, delays):
        ''' Set the delays '''
        print 'Set delays to %s' % delays
        #self.send_text_message('Delays were changed')


    def handle_tdc(self, message):
        ''' Process some timetags '''
        tag, data=message
        context = data['context']
        filename = data['filename']
        print 'Starting to postprocess (%s)...' % context
        time.sleep(2)
        count_rates = {'a':0, 'b':1}
        data={'context':context, 'count_rates': count_rates}
        self.pipe.send(('count_rates', data))
        print 'Finished postprocessing, wrote to disk etc'


    def shutdown(self, *args):
        ''' Close connection to DLL here '''
        print 'Shut down the postprocessor'
        sys.exit(0)
        


class coincidence_counter:
    ''' 
    An asynchrous coincidence counting system.
    Data aquisition and postprocessing run in parallel subprocesses.
    '''
    def __init__(self, callback=None):
        ''' Initialize both sub-processes '''
        # Create hook to SIGINT
        signal.signal(signal.SIGINT, self.shutdown)

        # Output of text
        self.callback=callback if callback else sys.stderr.write

        # Build the communication network
        self.pipe, post_pipe = Pipe()

        # Start up the postprocessing process
        self.post = Process(target=post, name='post', args=(post_pipe,))
        self.post.start()

        # Holder for latest count rates
        self.latest_count_rates=None


    def count(self, integration_time, context):
        ''' Count coincidences '''
        print 'Counting...'
        time.sleep(integration_time)
        print 'Done'
        self.pipe.send(('tdc', {'filename':'C:/awdawdawd/', 'context':context}))
        while self.pipe.poll():
            key, value = self.pipe.recv()
            if key=='count_rates': self.latest_count_rates=value


    def shutdown(self):
        ''' Shut down carefully '''
        print 'Shut down DPC230'
        self.pipe.send(('shutdown', None))
        

if __name__=='__main__':
    def callback(x):
        print x

    c=coincidence_counter(callback=callback)
    for position in range(5):
        c.count(5, {'position': position}) 
        print c.latest_count_rates
    c.shutdown()

    #for i in range(10):
        #c.count(5, context={'i':i})
        #print c.collect()

