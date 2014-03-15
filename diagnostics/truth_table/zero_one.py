from qy.hardware.heaters import dac, calibration_table
from qy.hardware.fpga import fpga
import numpy as np
from numpy import pi
import time
from qy.simulation import linear_optics as lo

def do_measurement(phases, ontime=1, offtime=12):
    voltages=table.get_voltages(phases)
    dac.write_voltages(voltages)
    print 'warming up...'
    for j in range(ontime): 
        fpga.read()
    counts=dict(zip(fpga.labels, fpga.read()))
    dac.zero()
    print 'cooling'
    for j in range(offtime): 
        fpga.read()
    return counts
    
class fake_fpga:
    def __init__(self):
        self.labels=['AB', 'AD', 'BC', 'CD']
             
    def read(self):
        time.sleep(1)
        return [0]*4
    
fpga=fake_fpga()
table=calibration_table()
dac=dac.dac()


for loop_index in range(1000):
   
    print '01'
    counts=do_measurement([0,pi,0,0,0,0,0,0])
    counts = np.array([counts['AB'], counts['AD'], counts['BC'], counts['CD']])
    



    
    