import time
from qy.hardware import dpc230
import qy.settings
import msvcrt

class hardware_server:
    ''' Talk to the DPC230 '''
    def __init__(self):
        ''' Set up defaults '''
        self.integration_time=1
        self.photon_buffer_switch=0
        self.photon_buffer_1=qy.settings.get('photon_buffer_1')
        self.photon_buffer_2=qy.settings.get('photon_buffer_2')
        self.connect_dpc230()

    def connect_dpc230(self):
        ''' Connect to the DPC230 '''
        self.dpc230=dpc230.dpc_daq(callback=self.counting_callback)
        self.dpc230.print_setup_summary()

    def disconnect_dpc230(self):
        ''' disconnect from the dpc230 '''
        self.dpc230.kill()

    def count_once(self):
        ''' The machine counts photons for one integration time '''

        # Choose a buffer
        which_buffer=self.photon_buffer_2 if self.photon_buffer_switch else self.photon_buffer_1
        print 'Acquiring timetags to %s...' % which_buffer,
        self.photon_buffer_switch = not self.photon_buffer_switch
        
        # Count for one second and send to postprocessor
        tdc1, tdc2 = self.dpc230.count(which_buffer, self.integration_time)
        #self.postprocessing_pipe.send({'tdc1':tdc1, 'tdc2':tdc2})
        print 'Done'

    def mainloop(self):
        ''' The main counting loop '''
        while not msvcrt.kbhit():
            self.count_once()
        self.disconnect_dpc230()

    def counting_callback(self, message):
        ''' Gets called by the counting system '''
        return True

if __name__=='__main__':
    h=hardware_server()
    h.mainloop()

