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


    def send_message(self, tag, data=None):
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

