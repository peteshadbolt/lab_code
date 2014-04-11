import numpy as np
from scipy.optimize import fmin
#from qy.hardware.heaters.fitting import *
from matplotlib import pyplot as plt

def plot_curve(parameter_space, data, style):
    plt.plot(parameter_space, data, style)
    plt.grid(linestyle='-', color='gray')
    plt.xlim(0, 7)
    
def phase_voltage(p, v): 
    ''' Phase as a function of voltage '''
    return p[0]+p[1]*(v**2)+p[2]*v

def counts_phase(phase,total_counts): 
    ''' Counts (intensity) as a function of phase '''
    return total_counts*(1-np.sin(phase/2)*np.sin(phase/2))

def counts_voltage(p, voltage, total_counts): 
    ''' Counts as a function of voltage '''
    return counts_phase(phase_voltage(p, voltage),total_counts)

def errfunc(p, voltage, count, total_counts): 
    ''' Error function, used in fitting '''
    return np.sum(np.power(counts_voltage(p, voltage, total_counts)-count, 2))

def fit_fringe(voltages, counts, total_counts, nfits=3, guess=None):
    ''' Fit a phase-voltage curve to some fringelike data '''
    # potentially choose a guess automatically
    if guess==None:
        p0 = np.array([0, .07, max(counts)])
    else:
        p0 = np.array(guess)

    # restart nelder-mead a few times
    for i in range(nfits):
        p0, best0, db, dc, warning = fmin(errfunc, p0, args=(voltages, counts,total_counts), disp=0, full_output=1)
    return p0
    
experiment_filename='data/6_experiment_wed26mar2014_1300pm.npy'
experiment=np.load(experiment_filename)

parameter_space_filename='data/6_parameters_wed26mar2014_1300pm.npy'
parameter_space=np.load(parameter_space_filename)

counts = experiment[:,3]
total_counts=experiment[:,4]
#print experiment
voltages = parameter_space
#guess=[pi,1,0]
guess=[ 0.93361981,0.09424765,0.37505169]
#guess=[1.28719277,0.1467268,0]
fitted_params=fit_fringe(voltages, counts, total_counts, guess=guess)
#fitted_params=guess
#fitted_params=[ -1.60789628+np.pi,0.14141038,1800,1]
print fitted_params
#fitted_params=guess

fit_space=np.linspace(0, 7, 40)
fit_counts=counts_voltage(fitted_params, fit_space,total_counts)

plt.subplot(211)
plot_curve(fit_space, fit_counts, 'r-')
plot_curve(voltages, counts, 'k.')

plt.subplot(212)
plt.text(0.05, 0.95, 'Total Counts', transform=plt.gca().transAxes, va='top')
plot_curve(voltages, total_counts, 'b.-')
plt.savefig('plots/alex_test_fit_wed26mar2014_1300pm.pdf')