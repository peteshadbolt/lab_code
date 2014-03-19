from qy.hardware.heaters import dac, calibration_table

d=dac.dac()
d.zero()
print 'zeroed the heaters'