from calibrate_and_fit import Calibrate
from sweep_fringe import take_fringe
from data_reader import load_data
from heaters import heaters
import numpy as np


def calibrate(reck_heaters, calib, heater_name, heater_index, input, outputs, minV, maxV, N, int_time):
	
	datafilename = take_fringe(reck_heaters, heater_index, minV, maxV, N, int_time)
	
	data_for_fitting = load_data(datafilename,outputs)
	voltages = np.linspace(minV, maxV, N)
	#calib.datafilename = data_for_fitting
	calib.fit(heatername, voltages, data_for_fitting)
	


	
if __name__ == '__main__':
	
	
	reck_heaters = heaters(port = 'COM10')
	reck_calib = Calibrate()
	#raw_input()
	#zero everything 
	#voltages = np.zeores([25])
	reck_heaters.zero()

	#set bias
	bias = 1
	reck_heaters.send_one_voltage(2, bias)

	#set Grounds, LED 
	reck_heaters.send_one_voltage(0, 0)
	reck_heaters.send_one_voltage(1, 0)
	reck_heaters.send_one_voltage(4, 0)
	reck_heaters.send_one_voltage(22, 0)

	minV = 0
	maxV = 1
	N = 2
	
	int_time = 1
	### Calibrate the first diagonal -----------------------------------------------
	# Get light going to the first diagonal
	for i in range(2):

		#p11 = heater driver 18
		calibrate(reck_heaters, reck_calib, 'p11', 1, 2, {'a':[]}, minV, maxV, N, int_time)
		reck_heaters.send_one_voltage((reck_calib.get_voltage_from_phase('p11',2*pi)), 1)


	reck_heaters.kill()
