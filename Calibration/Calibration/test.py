import numpy as np
import calibrate_and_fit
from calibrate_and_fit import Calibrate
reck_calib = Calibrate("C:\Users\ch8329\data1.txt")


def test():
	for i in range(2):
		reck_calib.fit('p11', graph = True)
		reck_calib.get_voltage_from_phase(1,2*np.pi)
	