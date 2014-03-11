from multiprocessing import Process, Pipe


class worker:
    ''' A generic worker process with TX/RX pipes '''
    def __init__(self, tx, rx):
        self.tx=tx
        self.rx=rx
        self.mainloop()

    def mainloop(self):
        ''' Keep on loopin '''
        while True:
            while self.rx.poll():
                message=self.rx.recv()
                self.handle_message(message)
                if message=='shutdown': return

    def handle_message(self, message):
        ''' Handle a message. This should be overridden '''
        output='%s got message "%s"' % (self.name, message)
        self.tx.send(output)


class daq(worker):
    ''' The data acquisition process '''
    def __init__(self, tx, rx):
        print 'Booting up data aquisition process'
        self.name='daq'
        worker.__init__(self, tx, rx)

    def handle_message(self, message):
        ''' Handle a message coming from the client ''' 
        if message[0]=='window': 
            print 'set window to X'
            self.tx.send('a')

        elif message[0]=='delays': 
            print 'set delays to X'
            self.tx.send('change the delays please')

        elif message[0]=='count': 
            print 'counting...'
            time.sleep(1)
            print 'done'
            self.tx.send('here are your tdc files')

        else:
            self.tx.send('done')

class post(worker):
    ''' The postprocessing process '''
    def __init__(self, tx, rx):
        print 'Booting up postprocessing process'
        self.name='post'
        worker.__init__(self, tx, rx)


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
        self.tx.send('awd')


    def collect(self):
        message=self.rx.recv()
        return message

if __name__=='__main__':
    c=coincidence_counter()
    c.send('awd')
    print c.collect()
    c.kill()
