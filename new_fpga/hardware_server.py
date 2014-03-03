import time
import numpy as np
from qython.hardware import fpga

class hardware_server:
    def __init__(self, postprocessing_pipe, gui_pipe):
        ''' connect to all of the relevant hardware '''
        self.postprocessing_pipe=postprocessing_pipe
        self.gui_pipe=gui_pipe
        self.alive=True
        self.connect_hardware()
        
    def mainloop(self):
        ''' the main counting loop '''
        while self.alive:
            self.integrate_once()
            self.check_messages()
        
        self.disconnect_hardware()
            
    def check_messages(self):
        ''' look for new messages '''
        while self.gui_pipe.poll():
            message=self.gui_pipe.recv()
            if 'quit' in message: self.alive=False
                    
        while self.postprocessing_pipe.poll():
            message=self.postprocessing_pipe.recv()
            
    def integrate_once(self):
        ''' integrates over many one-second integration blocks '''
        counts=self.fpga.read()
        counts=dict(zip(self.fpga.labels, counts))
        d={'count_rates': counts}
        self.postprocessing_pipe.send(d)
        
    def connect_hardware(self):
        ''' try to connect to all the relevant hardware '''
        self.fpga=fpga()
        
    def disconnect_hardware(self):
        ''' disconnect from all hardware '''
        self.fpga.kill()

if __name__=='__main__':
    x=hardware_server(None, None)
    x.integrate_once()
    

