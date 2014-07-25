#### Code that sweeps a fringe on a single heater and hold voltages constant on the others
import time, sys
import serial
from qy.hardware.dpc230 import coincidence_counter
from qy.formats import ctx
from qy.hardware import smc100
import qy.settings
import numpy as np

from pprint import pprint
from heaters import heaters
#from heater_class import heater

def handle_data(data):
		''' Define how to handle data coming from the counting system '''
		key, value = data
		#print data
		if key=='coincidence_data':
			# We got some count rates
			count_rates=value['count_rates']
			# together with the context in which they were measured
			context=value['context']
		
			# Print out some stuff
			print 'Recieved data for heater setting %s' % str(context[0])
			if 'n' in count_rates: print 'n: %d' % count_rates['n']
			
			# Write full context information to disk
			output_file.write('Heater context', context)
			# A less verbose alternative: 
			# output_file.write('position', context[which_motor]['position'])
			# Write count rates to disk
			output_file.write('count_rates', count_rates)

			
			
def take_fringe(reck_heaters, heater_index, min_voltage, max_voltage, N, int_time, metadata):
	
	global output_file
	output_file = ctx('C:/Users/Qubit/Code/lab_code/Calibration/Calibration/data/', metadata=metadata)	
	output_file_name = output_file.filename
	parameter_space=np.linspace(min_voltage, max_voltage, N)
	
	# Connect to the counting gear and configure it
	counter=coincidence_counter(callback=handle_data)
	counter.set_integration_time(int_time)

	for index, parameter in enumerate(parameter_space):
		print 'Setting voltage %s' % str(parameter)
		reck_heaters.send_one_voltage(heater_index, parameter)
		
		current_context=reck_heaters.dict()
		counter.count(context=current_context)
		
	# Collect and log the last piece of data from the postprocessor
	counter.collect()
	# Close connections to hardware
	counter.kill()
	
	return output_file_name

	
def plot_curve(parameter_space, data):
    plt.plot(parameter_space, data)
    plt.grid(linestyle='-')
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$'])
    plt.xlim(0, pi*2)
	