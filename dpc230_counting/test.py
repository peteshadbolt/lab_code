from multiprocessing import Process, Pipe 
import time, sys
from worker import worker

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
        #print 'Started counting'
        tag, data = message
        context = data['context']
        time.sleep(data['integration_time'])
        #print 'Finished counting'
        self.send_message('stop_daq')
        self.send_message('tdc', {'filename':'C:/awdawdawd/', 'context':context})


    def shutdown(self):
        ''' Close connection to DPC-230 here '''
        print 'Shut down the DAQ'
        sys.exit(0)


class post(worker):
    ''' The postprocessing process '''
    def __init__(self, tx, rx):
        self.name='post'
        worker.__init__(self, tx, rx)
        self.pass_on+=['count', 'stop_daq']
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
        #print '                   Starting to postprocess...'
        self.send_message('start_post')
        time.sleep(1)
        count_rates = {'a':0, 'b':1}
        #print '                   Finished postprocessing'
        self.send_message('stop_post')
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

        # Keep track
        self.n_daq=0
        self.n_post=0

    def send_message(self, tag, data):
        ''' Send a tag/data pair '''
        self.tx.send((tag, data))


    def count(self, integration_time, context):
        ''' Count coincidences '''
        self.n_daq+=1
        self.send_message('count', {'integration_time':integration_time,
                         'context': context})

    def collect(self):
        ''' Try to pick up some data '''
        while True:
            tag, data=self.rx.recv()
            print '\ngot message:', tag, data
            print 'before', self.n_daq, self.n_post
            if tag=='text': 
                callback(data)
            elif tag=='stop_daq': 
                print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa %d' % self.n_daq
                print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa %d' % self.n_post
                self.n_daq+=-1
            elif tag=='start_post': 
                self.n_post+=1
            elif tag=='stop_post': 
                self.n_post+=-1
            elif tag=='count_rates': 
                return data
            print 'after', self.n_daq, self.n_post

    def shutdown(self):
        ''' Shut down carefully '''
        self.send_message('shutdown', None)

if __name__=='__main__':
    def callback(x):
        print x

    c=coincidence_counter(callback=callback)
    for i in range(5):
        c.count(3, {'i_value': i}) 
        data=c.collect()
        #print 'Got %s back' % data
        #if qq: print qq
    qq = c.collect()
    #if qq: print qq
    c.shutdown()

    #for i in range(10):
        #c.count(5, context={'i':i})
        #print c.collect()

