import numpy as np
from qy.hardware.heaters import dac, calibration_table
from time import sleep
from numpy import pi
from powermeter import powermeter
from matplotlib import pyplot as plt

d=dac.dac()
d.zero()
print 'zeroed the heaters'