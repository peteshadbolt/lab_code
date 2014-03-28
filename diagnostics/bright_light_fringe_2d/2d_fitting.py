import numpy as np
from qy.hardware.heaters import dac, calibration_table
from time import sleep
from numpy import pi
from powermeter import powermeter
from matplotlib import pyplot as plt
from scipy.optimize import fmin
import sys

def fit_func(p, phases):
    full_contrast=(np.sin(phases[0]+p[0])*np.sin(phases[1]+p[1])+1)/2
    return p[2]*full_contrast+p[3]

def err_func(p, experiment, phases):
    theory=fit_func(p, phases)
    return np.sum((theory - experiment)**2)

def fit_to_data(experiment, parameter_space, guess=[0,0,1,0]):
    ''' Fit to some experimental data '''
    p1=fmin(err_func, guess, args=(experiment, parameter_space))
    return p1
    
def get_filenames(heater_indeces):
    data_filename='data/%d_%d.npy' % tuple(heater_indeces)
    param_filename='data/%d_%d_parameters.npy' % tuple(heater_indeces)
    return data_filename, param_filename

############ DATA ACQUISITION
def acquire_data(heater_indeces, N=20, DEBUG=False):
    min_phase, max_phase=0, 2*np.pi
    scan=np.linspace(min_phase, max_phase, N)
    parameter_space=np.meshgrid(scan, scan)    
    data=np.zeros([N,N])
    
    # connect hardware
    d=dac.dac()
    table=calibration_table()
    meter=powermeter()
        
    for index_1, parameter_1 in enumerate(scan):
        for index_2, parameter_2 in enumerate(scan):
            print index_1, index_2
            
            if DEBUG:
                data[index_1, index_2] = (1-index_1*.03)*fit_func([0.2,0.4,1,0], [parameter_1, parameter_2])
            else:
                # Figure out the settings
                voltages=np.zeros(8)
                first_heater, second_heater=heater_indeces
                voltages[first_heater]=table.get_voltage_from_phase(first_heater, parameter_1)
                voltages[second_heater]=table.get_voltage_from_phase(second_heater, parameter_2)
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
                data[index_1, index_2] = intensities[0]

    # Close hardware
    d.zero()
    meter.kill()
    
    # Normalize, save and return data
    data=data/np.amax(data)
    data_filename, param_filename = get_filenames(heater_indeces)
    np.save(data_filename, data)
    np.save(param_filename, parameter_space)
    return data_filename, param_filename

def plot_manifold(data):
    plt.imshow(data, extent=[0, 2*np.pi, 0, 2*np.pi], interpolation='nearest' )
    plt.grid(linestyle='-')
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$'])
    plt.yticks([0, np.pi/2, np.pi, 3*np.pi/2], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$'])
    plt.colorbar()

################################
heater_indeces=[1,3]

# Take data
acquire_data(heater_indeces, 20)

# Reload and fit
data_filename, param_filename = get_filenames(heater_indeces)
experiment=np.load(data_filename)
parameter_space=np.load(param_filename)
guess=[-np.pi/2+.3,-np.pi/2-.3, 1,0]
fitted_params=fit_to_data(experiment, parameter_space, guess=guess)
print 'Fit parameters:\n%s\n\n' % ('\n'.join(map(str, fitted_params)))

table=calibration_table()
for heater, fit_offset in zip(heater_indeces, fitted_params[:2]):
    print 'Existing offset for heater %d = %.5f' % (heater, table.get_parameters(heater)[0])
    print 'New DELTA for heater %d = %.5f' % (heater, fit_offset)
    print 
    
# Generate theory manifold and plot
theory=fit_func(fitted_params, parameter_space)
plt.subplot(121)
plot_manifold(experiment)
plt.subplot(122)
plot_manifold(theory)

plt.savefig('2d_sweep.pdf')

