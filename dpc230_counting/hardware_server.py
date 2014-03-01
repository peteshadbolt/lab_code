from time import sleep 
from qy.hardware import dpc230

class hardware_server:
    ''' Talk to the DPC230 '''
    def __init__(self):
        # Connect to the DPC230
		self.dpc230=dpc230.dpc_daq(callback=self.counting_callback)
		self.dpc230.print_setup_summary()
		self.photon_buffer_switch=0
		self.photon_buffer_1=qy.settings.get('photon_buffer_1')
		self.photon_buffer_2=qy.settings.get('photon_buffer_2')


    def mainloop(self):
        while True:
            print 'Hardware is sleeping...'
            sleep(2)


    def counting_callback(self, message):
        print message

if __name__=='__main__':
    hardware_server()
