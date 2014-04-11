import numpy as np
from qy.hardware.heaters import dac, calibration_table
from msvcrt import kbhit, getch
import sys

d=dac.dac()
table=calibration_table()

#use 3*np.pi/2

args = sys.argv[1:]
assert(len(sys.argv)-1) % 2 ==0
voltages=np.zeros(8)
for i in range(0, len(args), 2):
    index=int(args[i])
    phase=float(args[i+1])*np.pi
    voltage=table.get_voltage_from_phase(index,phase)
    voltages[index]=voltage
    print 'heater %d set to %.4f' % (index, phase)
    
d.write_voltages(voltages)

print 'press q to stop'
stop=False
while not stop:
    if kbhit(): stop = getch()=='q'
    
d.zero()