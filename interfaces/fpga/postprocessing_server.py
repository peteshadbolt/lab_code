import qy
import subprocess
import sys, os
import time

class postprocessing_server:
    def __init__(self, hardware_pipe, gui_pipe):
        ''' connect to all of the relevant hardware '''
        self.alive=True
        self.hardware_pipe=hardware_pipe
        self.gui_pipe=gui_pipe
        self.patterns=[]
                
    def check_messages(self):
        ''' check pipes for messages '''
        # check the pipe coming from the hardware system
        while self.hardware_pipe.poll():
            message = self.hardware_pipe.recv()
            if 'count_rates' in message: self.postprocess(message)
        
        # check the pipe coming from the gui
        while self.gui_pipe.poll():
            message = self.gui_pipe.recv()
            if 'quit' in message:   self.alive=False
            
    def postprocess(self, message):
        ''' postprocess some raw data '''
        count_rates=message['count_rates']
        self.gui_pipe.send({'count_rates':count_rates})
                
    def mainloop(self):
        ''' wait for commands '''
        while self.alive:
            self.check_messages()
