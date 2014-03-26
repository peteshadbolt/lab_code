import time, sys
from qy.hardware.dpc230 import coincidence_counter
from qy.gui.dpc230 import gui
from qy.formats import ctx


if __name__=='__main__':

    def handle_data(data):
        ''' Handles data from the counting system '''
        # Extract pertinent information
        key, value=data
        if key=='count_rates':
            interface.send('count_rates', value['count_rates'])

    def check_gui():
        ''' Check the state of the gui '''
        for key, value in interface.collect():
            if key=='gui_quit':
                counter.shutdown()
                sys.exit(0)
            elif key=='delays':
                counter.set_delays(value)
            elif key=='coincidence_window':
                counter.set_window(value)
            elif key=='integration_time':
                counter.set_integration_time(value)


    def dpc_callback(message):
        ''' Handles messages from the DPC230 '''
        interface.send('status', message)

    # The GUI
    interface=gui()

    # The counting gear
    counter=coincidence_counter(callback=handle_data, dpc_callback=dpc_callback)

    while True:
        counter.count({})
        check_gui()

    counter.shutdown()
    #interface.shutdown()

