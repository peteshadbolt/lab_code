from multiprocessing import Process, Pipe
import time

class worker:
    ''' A generic worker process with TX/RX pipes '''
    def __init__(self, tx, rx):
        self.tx=tx
        self.rx=rx
        self.pass_on=[]
        self.ignore=['ignore']

    def mainloop(self):
        ''' Keep on loopin '''
        while True:
            time.sleep(.1)
            while self.rx.poll():
                message=self.rx.recv()
                if message=='shutdown': 
                    self.tx.send('shutdown')
                    return
                else:
                    self.handle_message(message)

    def handle_message(self, message):
        ''' Handle a message. This should be overridden '''
        if message[0] in pass_on: 
            self.tx.send(message)
            return
        elif message[0] in ignore: 
            self.tx.send('ignored')
            return
        else:
            output='%s got message "%s"' % (self.name, message)
            self.tx.send(output)


class daq(worker):
    ''' The data acquisition process '''
    def __init__(self, tx, rx):
        #print 'Booting up data aquisition process'
        self.name='daq'
        worker.__init__(self, tx, rx)
        worker.pass_on=['window', 'delays', 'time_cutoff_ms']
        worker.mainloop()

    def handle_message(self, message):
        ''' Handle a message coming from the client ''' 
        if message[0]=='count': 
            print 'counting...'
            time.sleep(5)
            print 'done'
            self.tx.send(['tdc', 'awd'])

        else:
            self.tx.send('Unknown command')

class post(worker):
    ''' The postprocessing process '''
    def __init__(self, tx, rx):
        #print 'Booting up postprocessing process'
        self.name='post'
        worker.__init__(self, tx, rx)
        worker.ignore=['count']
        worker.mainloop()

    def handle_message(self, message):
        ''' Handle a message coming from the client ''' 
        if message[0]=='tdc': 
            self.handle_tdc(message[1])
        elif message[0]=='delays': 
            self.set_delays(message[1:])
        else:
            self.tx.send('Unknown command')

    def set_delays(self, delays):
        ''' Set the delays '''
            print 'Set delays to %s' % delays
            self.tx.send('Delays were changed')

    def handle_tdc(self, filename):
        ''' Process some timetags '''
            time.sleep(4)
            self.tx.send('here are your count rates')


class coincidence_counter:
    ''' 
    An asynchrous coincidence counting system.
    Data aquisition and postprocessing run in parallel subprocesses.
    '''
    def __init__(self):
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

    def send(self, message):
        self.tx.send(message)

    def collect(self):
        message=self.rx.recv()
        return message

    def shutdown(self):
        self.tx.send('shutdown')

if __name__=='__main__':
    c=coincidence_counter()

    c.send(['count', 5])
    for i in range(10):
        c.send(['count', 5])
        print c.collect()


    c.shutdown()
