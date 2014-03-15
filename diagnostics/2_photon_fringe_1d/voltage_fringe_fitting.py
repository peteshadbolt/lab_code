import numpy as np
from scipy.optimize import fmin
from qy.hardware.heaters.fitting import *
from matplotlib import pyplot as plt

def plot_curve(parameter_space, data, style):
    plt.plot(parameter_space, data, style)
    plt.grid(linestyle='-', color='gray')
    plt.xlim(0, 7)
    
    
experiment_filename='data/5_experiment_sat15mar2014_1640pm.npy'
experiment=np.load(experiment_filename)

parameter_space_filename='data/5_parameters_sat15mar2014_1640pm.npy'
parameter_space=np.load(parameter_space_filename)

counts = experiment[:,0]
voltages = parameter_space
#guess=[pi,1,0]
fitted_params=fit_fringe(voltages, counts)

print fitted_params
fit_space=np.linspace(0, 7, 300)
fit_counts=counts_voltage(fitted_params, fit_space)

plot_curve(fit_space, fit_counts, 'r-')
plot_curve(voltages, counts, 'k.')
plt.savefig('plots/fit.pdf')