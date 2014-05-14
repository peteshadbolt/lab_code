import time, sys
from qy.hardware.dpc230 import coincidence_counter
from qy.formats import ctx
from qy.hardware import smc100
import qy.settings
import numpy as np

''' 
An example of dip-taking, without a GUI 
'''


if __name__=='__main__':
    
    def handle_data((key, value)):
        ''' Define how to handle data coming from the counting system '''
        if key=='coincidence_data':
            # We got some count rates
            count_rates=value['count_rates']
            # together with the context in which they were measured
            context=value['context']

            # Print out some stuff
            print 'Recieved data for actual position %.3f' % context[which_motor]['position']
            if 'n' in count_rates: print 'n: %d' % count_rates['n']
            
            # Write full context information to disk
            output_file.write('context', context)
            # A less verbose alternative: 
            # output_file.write('position', context[which_motor]['position'])
            # Write count rates to disk
            output_file.write('count_rates', count_rates)

        elif key=='dpc230_status':
            pass


    ##################################################### 
    # START HERE 
    ##################################################### 

    # Get a file ready to store data
    metadata={'label':'This is a test!', 'mood':'hungry for knowledge'}
    output_file=ctx('C:/Users/Qubit/Desktop/data_from_example_scripts/', metadata=metadata)

    # Dip parameters
    parameter_space = np.linspace(0, 10, 11)
    which_motor=3 

    # Connect to the motor controllers
    motor_controller=smc100(callback=None)

    # Connect to the counting gear and configure it
    counter=coincidence_counter(callback=handle_data)
    counter.set_integration_time(1)

     # Loop over a dip
    for position in parameter_space:
        print 'Moving to position %.3f' % position
        motor_controller.actuators[which_motor].move(position)
        current_context=motor_controller.dict()
        counter.count(context=current_context)

    # Collect and log the last piece of data from the postprocessor
    counter.collect()

    # Close connections to hardware
    counter.kill()
    motor_controller.kill()

