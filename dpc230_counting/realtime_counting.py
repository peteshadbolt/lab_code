
import time, sys
from qy.hardware.wrappers.coincidence_counter import threaded_coincidence_counter
from qy.hardware.wrappers.photon_elf import threaded_photon_elf
from qy.formats import ctx
        

if __name__=='__main__':

    def handle_data(data):
        ''' Handles data from the counting system '''
        # Extract pertinent information
        key, value=data

        data = elf.recv()
        if data!=None and data[0]=='gui_quit':
            counter.shutdown()
            sys.exit(0)

        if key=='count_rates': 
            elf.send('count_rates', value['count_rates'])

    def dpc_callback(message):
        ''' Handles messages from the DPC230 '''
        elf.send('status', message)

    # The GUI
    elf=threaded_photon_elf()

    # The counting gear
    counter=threaded_coincidence_counter(callback=handle_data, dpc_callback=dpc_callback)

    while True:
        counter.count(1, {}) 

    counter.shutdown()
    #elf.shutdown()

