import numpy as np
from qy.hardware.heaters import dac, calibration_table
from time import sleep
from numpy import pi
from powermeter import powermeter
from matplotlib import pyplot as plt
from scipy.optimize import fmin
import sys

def fit_func(p, phase):
    ''' Fit to a sinusoid '''
    full_contrast=(np.sin(phase+p[0])+1)/2
    return p[1]*full_contrast+p[2]

def err_func(p, phase, count): 
    ''' Error function, used in fitting '''
    return np.sum((fit_func(p, phase)-count)**2)

def fit_to_data(experiment, parameter_space, guess=[0,1,0]):
    ''' Fit to some experimental data '''
    print err_func(guess, parameter_space, experiment)
    p1=fmin(err_func, guess, args=(parameter_space, experiment))
    print err_func(p1, parameter_space, experiment)
    return p1
    
def get_filenames(heater_index):
    data_filename='data/%d.npy' % (heater_index,)
    param_filename='data/%d_parameters.npy' % (heater_index,)
    return data_filename, param_filename

############ DATA ACQUISITION
def acquire_data(heater_index, N=20, DEBUG=False, hold=[]):
    min_phase, max_phase=0, 2*np.pi
    parameter_space=np.linspace(min_phase, max_phase, N)
    data=np.zeros([N])
    
    # connect hardware
    d=dac.dac()
    table=calibration_table()
    meter=powermeter()
        
    for index_1, parameter_1 in enumerate(parameter_space):
        print index_1
        
        if DEBUG:
            data[index_1] = 0
        else:
            # Figure out the settings
            voltages=np.zeros(8)
            voltages[heater_index]=table.get_voltage_from_phase(heater_index, parameter_1)

            # Hold some phases constant during the scan
            for index, phase in hold:
                voltages[index]=table.get_voltage_from_phase(index, phase)
                
            print voltages.round(3)
            
            # Do the measurement
            d.write_voltages(voltages)
            for q in range(10):
                meter.read()
            intensities=np.zeros(6)
            for q in range(6):
                intensities+=np.array(meter.read())
            # cool
            d.zero()
            for q in range(10):
                meter.read()
            data[index_1] = intensities[0]

    # Close hardware
    d.zero()
    meter.kill()
    
    # Normalize, save and return data
    data=data/np.amax(data)
    data_filename, param_filename = get_filenames(heater_index)
    np.save(data_filename, data)
    np.save(param_filename, parameter_space)
    return data_filename, param_filename

def plot_curve(parameter_space, data, style):
    plt.plot(parameter_space, data, style)
    plt.grid(linestyle='-')
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$'])
    plt.xlim(0, pi*2)

################################
heater_index = 4
hold_table=[[0,pi/2],[2,0], [6,pi/2]]

# Take data
acquire_data(heater_index, hold=hold_table, N=20)

# Reload and fit
data_filename, param_filename = get_filenames(heater_index)
experiment=np.load(data_filename)
parameter_space=np.load(param_filename)

guess=[0,.6,.4]
fitted_params=fit_to_data(experiment, parameter_space, guess=guess)
#fitted_params=guess
#fitted_params=[0,1,0]

print 'Fit parameters:\n%s\n\n' % ('\n'.join(map(str, fitted_params)))

table=calibration_table()
print 'Existing offset for heater %d = %.5f' % (heater_index, table.get_parameters(heater_index)[0])
print 'New DELTA for heater %d = %.5f' % (heater_index, fitted_params[0])
print 
    
# Generate theory manifold and plot
theory_space=np.linspace(0, 2*pi, 300)
theory=fit_func(fitted_params, theory_space)
plt.subplot(121)
plot_curve(parameter_space, experiment, 'k.-')
plt.subplot(122)
plot_curve(theory_space, theory, 'k-')

plt.savefig('1d_sweep.pdf')

