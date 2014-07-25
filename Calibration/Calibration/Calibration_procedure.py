from calibrate_and_fit import Calibrate
from sweep_fringe import take_fringe
from reader import load_data
from heaters import heaters
from heater_class import heater



def calibrate(reck_heaters, calib, heater_name, heater_index, input, outputs):
	
	datafilename = take_fringe(reck_heaters, heater_index)
	
	data_for_fitting = load_data(datafilename,outputs)
	
	calib.datafilename = data_for_fitting
	calib.fit(heatername)
	


	
if __name__ == '__main__':
	
	
	reck_heaters = heaters(port = 'COM10')
	reck_calib = Calibrate()
	
	
	#zero everything 
	voltages = np.zeores([25])
	reck_heaters.send_voltages(voltages)
	
	#set bias
	bias = 1
	reck_heaters.send_one_voltage(2, bias)
	
	#reck_heaters.send_one_voltage(0, 0)
	#reck_heaters.send_one_voltage(1, 0)
	#reck_heaters.send_one_voltage(4, 0)
	#reck_heaters.send_one_voltage(21, 0)
	
  ### Calibrate the first diagonal -----------------------------------------------
  # Get light going to the first diagonal
  for i in range(2):
  
	#p11 = heater driver 18
    calibrate(reck_heaters, reck_calib, 'p11', 18, 2, {'a':[]})
	reck_heaters.send_one_voltage(18,(reck_calib.get_voltage_from_phase('p11',2*pi)))
	
    calibrate(c, r15, v, 2, (0,), count*time)
    r15.set_phase(2*pi)
	
    calibrate(c, r25, v, 2, (1,2,3,4,5), count*time)
    r25.set_phase(pi)
    calibrate(c, r15, v, 2, (0,), count*time)
    r15.set_phase(2*pi)
    calibrate(c, r05, v, 2, (0,), count*time)
    r05.set_phase(2*pi)
  
  # Calibrate the other heaters
  r05.set_phase(pi)
  calibrate(c, r04, v, 2, (2,3,4,5), count*time)
  r04.set_phase(2*pi)
  calibrate(c, r03, v, 2, (3,4,5), count*time)
  r03.set_phase(2*pi)
  calibrate(c, r02, v, 2, (4,5), count*time)
  r02.set_phase(2*pi)
  calibrate(c, r01, v, 2, (5,), count*time)

### Calibrate the second diagonal ----------------------------------------------
  # Get light going to the second diagonal
  r04.set_phase(pi)
  r03.set_phase(pi)
  r02.set_phase(pi)
  r01.set_phase(pi)
  r15.set_phase(pi)

  # Calibrate the other heaters
  calibrate(c, r14, v, 2, (3,4,5), count*time)
  r14.set_phase(2*pi)
  calibrate(c, r13, v, 2, (4,5), count*time)
  r13.set_phase(2*pi)
  calibrate(c, r12, v, 2, (5,), count*time)

### Calibrate the third diagonal -----------------------------------------------
  # Get light going to the third diagonal
  r14.set_phase(pi)
  r13.set_phase(pi)
  r12.set_phase(pi)
  r25.set_phase(2*pi)

  # Calibrate the other heaters
  calibrate(c, r24, v, 2, (4,5), count*time)
  r24.set_phase(2*pi)
  calibrate(c, r23, v, 2, (5,), count*time)

### Calibrate the phases ------------------------------
  
  #phi12 - BS: r12, r01#
  r23.set_phase(pi)
  r12.set_phase(pi/2)
  r01.set_phase(pi/2)
  calibrate(c, phi12, v, 2, (5,), count*time, shift=pi, graph = True)
  phi12.set_phase(2*pi)
  r12.set_phase(pi)
  r01.set_phase(pi)
  
  #phi23 - BS: r23, r12.  No need to set r12#
  r23.set_phase(pi/2)
  calibrate(c, phi23, v, 2, (5,), count*time, shift=pi, graph = True)
  phi23.set_phase(2*pi)
  r23.set_phase(pi)
  r12.set_phase(pi)
  
  #phi13 - BS: r13, r02.  Heater r03 and r12 have already been set to pi#
  r24.set_phase(pi)
  r13.set_phase(pi/2)
  r02.set_phase(pi/2)
  calibrate(c, phi13, v, 2, (4,), count*time, graph=True)
  phi13.set_phase(2*pi)
  r02.set_phase(pi)
  
  #phi24 - BS: r24, r13. No need to set r13#
  r24.set_phase(pi/2)
  calibrate(c, phi24, v, 2, (4,), count*time, graph = True)
  phi24.set_phase(2*pi)
  r24.set_phase(pi)
  r13.set_phase(pi)
  
  #phi14 - BS: r03, r14.
  r25.set_phase(pi)
  r14.set_phase(pi/2)
  r03.set_phase(pi/2)
  calibrate(c, phi14, v, 2, (3,), count*time)
  phi14.set_phase(2*pi)
  r03.set_phase(pi)
  
  #phi25 - BS: r14, r25. No need to set r14
  r25.set_phase(pi/2)
  calibrate(c, phi25, v, 2, (3,), count*time)
  phi25.set_phase(2*pi)
  r25.set_phase(pi)
  r14.set_phase(pi)
  
  #phi15
  r15.set_phase(pi/2)
  r04.set_phase(pi/2)
  calibrate(c, phi15, v, 2, (1,), count*time)
  phi15.set_phase(2*pi)
  r13.set_phase(pi)
  r02.set_phase(pi)