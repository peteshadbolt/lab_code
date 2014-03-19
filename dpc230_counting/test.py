from multiprocessing import Process, Pipe 
import time, sys
import signal

class worker:
    ''' A generic worker process with TX/RX pipes '''
    def __init__(self, tx, rx):
        self.tx=tx
        self.rx=rx
        self.pass_on=['text']
        self.name='Worker process'
        # Create hook to SIGINT
        signal.signal(signal.SIGINT, self.signal_handler)


    def mainloop(self):
        ''' Keep on looping '''
        while True:
            time.sleep(.1)
            while self.rx.poll():
                message=self.rx.recv()
                self.meta_handle_message(message)


    def meta_handle_message(self, message):
        ''' Handle or ignore a message. '''
        if message[0]=='shutdown': 
            self.tx.send(message)
            self.shutdown()
        elif message[0] in self.pass_on: 
            self.tx.send(message)
        else:
            self.handle_message(message)


    def handle_message(self, message):
        ''' Handle a message which cannot be passed on '''
        tag, data = message
        self.send_text_message('%s got a message: %s: %s' % (self.name, tag, data))


    def send_message(self, tag, data):
        ''' Send a tag/data pair '''
        self.tx.send((tag, data))


    def send_text_message(self, text):
        ''' Send a plain text message, which will bubble up to the main process '''
        self.send_message('text', text)


    def signal_handler(self, signal, frame):
        ''' Try to handle SIGINT signals gracefully '''
        self.shutdown()


    def shutdown(self):
        ''' Shut everything down '''
        print 'Shut down %s' % self.name
        sys.exit(0)



class daq(worker):
    ''' The data acquisition process '''
    def __init__(self, tx, rx):
        worker.__init__(self, tx, rx)
        self.name='daq'
        self.pass_on=['window', 'delays', 'time_cutoff_ms']
        self.send_text_message('Booting up DAQ...')
        self.mainloop()


    def handle_message(self, message):
        ''' Handle a message coming from the client ''' 
        if message[0]=='count': 
            self.count(message)


    def count(self, message):
        ''' Initiate coincidence-counting '''
        tag, data = message
        context = data['context']
        self.send_text_message('Starting to count...')
        time.sleep(data['integration_time'])
        self.send_text_message('Finished counting')
        self.send_message('tdc', \
                {'filename':'C:/awdawdawd/', 'context':context})


    def shutdown(self):
        ''' Close connection to DPC-230 here '''
        print 'Shut down the DAQ'
        sys.exit(0)



class post(worker):
    ''' The postprocessing process '''
    def __init__(self, tx, rx):
        self.name='post'
        worker.__init__(self, tx, rx)
        self.pass_on+=['count', 'finished_counting']
        self.send_text_message('Booting up postprocessing...')
        self.mainloop()


    def handle_message(self, message):
        ''' Handle a message coming from the client ''' 
        if message[0]=='tdc': 
            self.handle_tdc(message)
        elif message[0]=='delays': 
            self.set_delays(message[1])


    def set_delays(self, delays):
        ''' Set the delays '''
        print 'Set delays to %s' % delays
        self.send_text_message('Delays were changed')


    def handle_tdc(self, message):
        ''' Process some timetags '''
        tag, data=message
        context = data['context']
        filename = data['filename']
        self.send_text_message('Starting to postprocess...')
        time.sleep(1)
        count_rates = {'a':0, 'b':1}
        self.send_text_message('Finished postprocessing')
        self.send_message('count_rates', \
                {'count_rates':count_rates, 'context':context})


    def shutdown(self):
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
        # Keep track of counting
        self.pending_requests=0

        # Output of text
        self.callback=callback if callback else sys.stderr.write

        # Generate the communication network
        self.tx, daq_rx = Pipe()
        daq_tx, post_rx = Pipe()
        post_tx, self.rx = Pipe()

        # Start up the data acquisition process
        self.daq = Process(target=daq, name='daq', args=(daq_tx, daq_rx))
        self.daq.start()

        # Start up the postprocessing process
        self.post = Process(target=post, name='post', args=(post_tx, post_rx))
        self.post.start()

    def send_message(self, tag, data):
        ''' Send a tag/data pair '''
        self.tx.send((tag, data))


    def count(self, integration_time, context):
        ''' Count coincidences '''
        self.send_message('count', {'integration_time':integration_time,
                         'context': context})
        self.pending_requests+=1

    def collect(self):
        ''' Try to pick up some data '''
        if self.pending_requests==1: 
            print 'only had one pending request'
            return None
        while True:
            tag, data=self.rx.recv()
            if tag=='text': 
                callback(data)
            elif tag=='count_rates': 
                self.pending_requests+=-1
                return data

    def shutdown(self):
        ''' Shut down carefully '''
        self.send_message('shutdown', None)

if __name__=='__main__':
    def callback(x):
        pass

    c=coincidence_counter(callback=callback)
    for i in range(5):
        position=5+i/10.
        print 'moved motor controller to %.1f' % position
        c.count(1, {'mc_position': position}) 
        print c.collect()
    print c.collect()

    print 'doing something else...'
    time.sleep(5)
    print 'done'

    for i in range(5):
        position=5+i/10.
        print 'moved motor controller to %.1f' % position
        c.count(1, {'mc_position': position}) 
        print c.collect()
    print c.collect()

    c.shutdown()

    #for i in range(10):
        #c.count(5, context={'i':i})
        #print c.collect()

