from calibrate_and_fit import Calibrate
from sweep_fringe import take_fringe
from powermeter_fringe import pm_take_fringe
from parse_data import parse
from heaters import heaters
import numpy as np

from qy.formats import ctx
from qy.analysis.coincidence_counting.pattern_parser import parse_coincidence_pattern

def calibrate(reck_heaters, calib, heater_name, heater_index, input, outputs, minV, maxV, N, int_time, counting):

    metadata={'label':'Fringe Sweep', 'Counting Device': counting, 'heater': (heater_index, heater_name), 'Input': input, 'Outputs': outputs, 'Int_time': int_time, 'MinV': minV, 'MaxV': maxV}
    
    if counting == 'cc': 
        datafilename = take_fringe(reck_heaters, heater_index, minV, maxV, N, int_time, metadata)
    elif counting == 'pm':
        datafilename = pm_take_fringe(reck_heaters, heater_index, minV, maxV, N, int_time, metadata)
    
    data_for_fitting = parse(datafilename,outputs)



    voltages = np.linspace(minV, maxV, N)
    #calib.datafilename = data_for_fitting
    calib.fit(heater_index, voltages, data_for_fitting, graph = True)




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

    minV = 0.
    maxV = 12
    N = 25

    int_time = 10
    ### Calibrate the first diagonal -----------------------------------------------
    # Get light going to the first diagonal

    
    #p11 = heater driver 18
    calibrate(reck_heaters, reck_calib, 'p11', 18, 2, ('a'), minV, maxV, N, int_time, 'pm')
    #reck_heaters.send_one_voltage(18,(reck_calib.get_voltage_from_phase(18,2*np.pi)))
    #print reck_heaters.send_one_voltage(18,(reck_calib.get_voltage_from_phase(18,2*np.pi)))

    phase=[]
    volts = np.linspace(minV, maxV, N)
    for i in range(len(volts)):
        phase.append(reck_calib.get_phase_from_voltage(18, volts[i]))
    
    plt.plot(volts, phase)
    plt.show()

    reck_heaters.kill()
