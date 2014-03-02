from qy.hardware import dpc230
import qy.settings

class easy_dpc:
    ''' Talk to the DPC230 with less overhead '''
    def __init__(self, callback):
        ''' Set up defaults '''
        self.integration_time=1
        self.photon_buffer_switch=0
        self.photon_buffer_1=qy.settings.get('photon_buffer_1')
        self.photon_buffer_2=qy.settings.get('photon_buffer_2')
        self.dpc230=dpc230.dpc_daq(callback=callback)


    def count_once(self):
        ''' The machine counts photons for one integration time '''
        # Choose a buffer
        which_buffer=self.photon_buffer_2 if self.photon_buffer_switch else self.photon_buffer_1
        self.photon_buffer_switch = not self.photon_buffer_switch
        tdc1, tdc2 = self.dpc230.count(which_buffer, self.integration_time)
        return tdc1, tdc2


    def kill(self):
        ''' Close connection '''
        self.dpc230.kill()
    

