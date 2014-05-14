import time, sys
from qy.hardware.dpc230 import coincidence_counter
from qy.gui.dpc230 import gui
from qy.formats import ctx


if __name__=='__main__':

    def handle_data((key, value)):
        ''' Handles data from the counting system '''
        # Pass the message on to the GUI
        if key=='coincidence_data':
            interface.send('count_rates', value['count_rates'])
        elif key=='dpc230_status':
            interface.send('status', value)

    def check_gui():
        ''' Check the state of the gui '''
        for key, value in interface.collect():
            if key=='gui_quit':
                counter.kill()
                sys.exit(0)
            elif key=='delays':
                counter.set_delays(value)
            elif key=='coincidence_window':
                counter.set_window(value)
            elif key=='integration_time':
                counter.set_integration_time(value)

    # Make the GUI
    interface=gui()

    # Boot up the counting gear
    counter=coincidence_counter(callback=handle_data)

    # Loop forever
    while True:
        counter.count({})
        check_gui()


