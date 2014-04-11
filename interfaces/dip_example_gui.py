import time, sys
from qy.hardware.dpc230 import coincidence_counter
from qy.formats import ctx
from qy.hardware import smc100
from qy.gui.coincidence_counting import gui
import qy.settings
import numpy as np

''' 
An example of dip-taking, with a GUI 
'''


if __name__=='__main__':
    
    def handle_data(data):
        ''' Define how to handle data coming from the counting system '''

        key, value = data

        if key=='count_rates':
            # We got some count rates
            count_rates=value['count_rates']
            # together with the context in which they were measured
            context=value['context']

            # Print out some stuff
            print 'Recieved data for actual position %.3f' % context[which_motor]['position']
            if 'n' in count_rates: print 'n: %d' % count_rates['n']
            
            # Just write the position to the file
            output_file.write('position', context[which_motor]['position'])

            # Write count rates to disk, and also forward them to the GUI
            interface.send('count_rates', count_rates)
            output_file.write('count_rates', count_rates)


    def dpc_callback(message):
        ''' Passes on messages from the DPC230 to the GUI'''
        interface.send('status', message)

    ##################################################### 
    # START HERE 
    ##################################################### 

    # Dip parameters
    parameter_space = np.linspace(0, 10, 11)
    which_motor=3 

    # Get a file ready to store data
    md={'label':'This is a test!', 'mood':'hungry for knowledge'}
    output_file=ctx('C:/Users/Qubit/Desktop/data_from_example_scripts/', metadata=md)

    # Make the GUI
    interface=gui()

    # Connect to the motor controllers
    motor_controller=smc100(callback=None)

    # Connect to the counting gear and configure it
    counter=coincidence_counter(callback=handle_data, dpc_callback=dpc_callback)
    counter.set_integration_time(1)

     # Loop over a dip
    for position in parameter_space:
        print 'Moving to position %.3f' % position
        motor_controller.actuators[which_motor].move(position)
        current_context=motor_controller.dict()
        counter.count(context=current_context)

    # Collect and log the last piece of data from the postprocessor
    counter.collect()

    # Close connections to hardware and GUI
    counter.kill()
    motor_controller.kill()
    interface.kill()

