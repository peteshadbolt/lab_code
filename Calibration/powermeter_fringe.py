#### Code that sweeps a fringe on a single heater and hold voltages constant on the others
import time, sys
import serial
from qy.hardware.powermeter import powermeter
from qy.formats import ctx

import qy.settings
import numpy as np

from pprint import pprint
from heaters import heaters


    
    
        
                
                
def pm_take_fringe(reck_heaters, heater_index, min_voltage, max_voltage, N, int_time, metadata):

    pm=powermeter()
    keys = ['a','b','c','d','e','f']
    
    #global output_file
    output_file = ctx('C:/Users/Qubit/Code/lab_code/Calibration/Calibration/data/', metadata=metadata)	
    output_file_name = output_file.filename

    parameter_space=np.linspace(min_voltage, max_voltage, N)


    for index, parameter in enumerate(parameter_space):
        
        print 'Setting voltage %s' % str(parameter)
        reck_heaters.send_one_voltage(heater_index, parameter)
        time.sleep(1)
        total=np.zeros(6)
        
        print reck_heaters.query_v(heater_index)
        print pm.read()
        
        for i in range(int_time):
            total += np.array(pm.read())
        
        print total
        
        counts_dict = dict(zip(keys, total.tolist()))
        output_file.write('count_rates', counts_dict)
        current_context=reck_heaters.vip_heater(heater_index)
        output_file.write('context', current_context)
        
    pm.kill()

    return output_file_name


	