#### Code that sweeps a fringe on a chosen heater, whilst holding the voltage on other heaters constant.
#### Then fits to this data and stores the fitted parameters to disk.  
import math
import numpy as np
from numpy import pi
from matplotlib import pyplot as plt
from scipy.optimize import fmin
import qy
import qy.settings
from qy.util import json_no_unicode
import os, json
from scipy.optimize import fsolve
import scipy.optimize as opt


def phase_volatge(p, v): p[2]  + p[3]*np.power(v,2) + p[4]*np.power(v,3)
def err(p, v, data): return np.sum( np.power((fitfunc(p,v) - data),2) )
def fitfunc(p, v): 
	return p[0] + p[1]*np.cos(p[4]*np.power(v,3) + p[3]*np.power(v,2) + p[2])
	#return p[0]*(1 - p[1]*np.power(np.cos((p[2] + p[3]*np.power(v,2) + p[4]*np.power(v,3))/2),2))
def fitfunc2(v, off, amp, const, quad, cub): 
	return off + amp*np.cos(cub*np.power(v,3) + quad*np.power(v,2) + const)
	#return off*(1 - amp*np.power(np.cos((const + quad*np.power(v,2) + cub*np.power(v,3))/2),2))
def func(p,phase): return p[0]*(1 - p[1]*np.power(np.cos((phase)/2),2))
#def fitfunc(p, v): return p[0]*(1 + p[1]*np.power(np.sin((p[2]  + p[3]*np.power(v,2))),2))

class Calibrate:

	def __init__(self, datafilename=None, paramfilename=None):
		self.dir = os.path.dirname(os.path.realpath(__file__))
		if paramfilename==None: paramfilename = os.path.join(self.dir, 'heater_calibration.json')
		self.paramfilename = paramfilename
		self.datafilename = datafilename
		self.data = []
		self.curve_parameters={}
		if os.path.exists(self.paramfilename): self.load()

	def load(self, filename=None):
		''' Load the data from a JSON file on disk '''
		#dir = os.path.dirname(os.path.realpath(__file__))
		#jfile = os.path.join(dir, 'data\heater_calibration.json')
		f=open(self.paramfilename, 'r')
		data=json.loads(f.read(), object_hook=json_no_unicode)
		f.close()
		self.curve_parameters=data['curve_parameters']
		self.heater_count=len(self.curve_parameters)		

	def save(self, heater_index, params):
		'''Save the parameters to JSON file on disk'''
		self.curve_parameters={key: tuple(value) for key, value in self.curve_parameters.items()}
		d = {'heater_count': len(self.curve_parameters), 'curve_parameters': self.curve_parameters}
		f = open(self.paramfilename, 'w')
		#print d
		#raw_input()
		f.write(json.dumps(d, indent=4, sort_keys=True))
		f.close()

	def get_parameters(self, heater_index):
		''' Get the full set of parameters for a particular heater'''
		try:
			p=self.curve_parameters[heater_index]
		except KeyError:
			p=self.curve_parameters[unicode(heater_index)]
		return p
	
	def load_data(self):
		'''Loads data required to perform fit'''
		self.data = np.loadtxt(self.datafilename, delimiter=',')
		return self.data
	
	def read_data(self):
		'''reads in data required to perform fits'''
		self.load_data()
		voltages = []
		I1 = []
		for i in range(len(self.data)):
			voltages.append(self.data[i][0])
			I1.append(self.data[i][3])
		return voltages, I1

	def fit(self, heater_index, voltages, I, graph=False):
		''' perform least squares fit to data, loop over fit a few times
		to ensure convergence to correct result. Needs help with sensible guess
		Note: the unicode(heater...) is required to avoid repeated heater indices in json file.'''
		
		#voltages, I = self.read_data()
		lo=min(I)
		hi=max(I)
		offset=lo
		amplitude=(hi-lo)
		cubic=0.00003
		quad=0.04
		const=2*np.arccos(np.sqrt((I[0]-offset)/amplitude))
		
		p0=[offset, amplitude, const, quad, cubic]
		for i in range(0,5):
			p1 = fmin(err, p0, args=(voltages, I), disp=0)
			p0 = p1
		
		'''
		p0=[offset, amplitude, const, quad, cubic]
		popt,pcov = opt.curve_fit(fitfunc2,voltages,I,p0)
		print p1 - popt
		raw_input()
		# Plot the graph if requested
		'''
		self.curve_parameters[unicode(heater_index)] = p1
		#print heater_index
		#print self.curve_parameters
		self.save(heater_index,p1)
		
		if graph:
			self.plot(p1, I, voltages, heater_index)
		
		return p1
		
	def get_phase_from_voltage(self, heater_index, v):
		p=self.get_parameters(heater_index)
		phase = p[2] + p[3]*np.power(v,2) + p[4]*np.power(v,3)
		return phase
	
	def phi_func(self,v,phase,p):
		y= p[2] + p[3]*(v**2) + p[4]*(v**3) - phase 
		return y
	
	def get_voltage_from_phase(self, heater_index, phase, guess = 0, initial=True):
		''' Get the appropriate voltage to set to the chip, given a phase '''
		'''Assuming that phi=a+b*v^2+c*v**3'''
		guess = 0
		p=self.get_parameters(heater_index)
		v = fsolve(self.phi_func, guess, args=(phase,p))
		while v < 0:
			print 'Error: negative voltage'
			guess += 5
			v = fsolve(self.phi_func, guess, args=(phase,p))
		#print p
		#print phase
		#print p[2] + p[3]*(v[0]**2) + p[4]*(v[0]**3)
	
		'''
		raw_input()
		if v[0] > 0 and v[0] < 11:
			#print abs(self.phi_func(v[0],phase,p))%(2*np.pi)
			if (abs(self.phi_func(v[0],phase,p))%(2*np.pi) > 0.00001):
				#print 'fuckup'
				#print heater_index
				#print phase
				#print v[0]
				#print abs(self.phi_func(v[0],phase,p))%(2*np.pi)
				#print 'guess=%f' % guess
				guess=np.random.uniform(0,12)
				phase+=2*np.pi
				#print 'fixing...'
				return self.get_voltage_from_phase(heater_index,phase, guess,initial=False)
			else:
				return v[0]
		elif v[0] > 11:
			#print '>7 loop'
			phase-=2*np.pi
			guess=np.random.uniform(0,12)
			return self.get_voltage_from_phase(heater_index,phase, guess,initial=False)
		else:
			#print '<0 loop'
			phase+=2*np.pi
			guess=np.random.uniform(0,12)
			return self.get_voltage_from_phase(heater_index,phase, guess,initial=False)

		'''
		return v[0]
		
	def get_voltage_from_phase_old(self, heater_index, phase):
		''' Get the appropriate voltage to set to the chip, given a phase '''
		'''Assuming that phi=a+b*v^2'''
		p=self.get_parameters(heater_index)
		phase=phase%(2*np.pi)

		if p[3] < 0 and (phase-p[2]) > 0:
			while phase-p[2] > 0: phase-=2*np.pi
		elif p[3] > 0 and (phase-p[2])<0:
			while phase-p[2] > 0: phase+=2*np.pi
		else:
			v=np.sqrt((phase-p[2])/p[3])
			return v
		v=np.sqrt((phase-p[2])/p[3])
		return v
		
	def plot(self, params, counts, voltages, heater_index):
		print heater_index
		v = np.linspace(-15,15,10000)
		plt.plot(v,fitfunc(params,v), label = 'Fit')
		plt.plot(voltages,counts,'x', marker = '+', markersize = 5,label = 'data')
		plt.xlabel('Voltage, V', fontsize = 20)
		plt.ylabel('Normalised Intensity', fontsize = 20)
		plt.legend()
		plt.savefig(os.path.join(self.dir,'plots/' + str(heater_index) + '.png'))
		plt.show()
		#plt.clf()
	
