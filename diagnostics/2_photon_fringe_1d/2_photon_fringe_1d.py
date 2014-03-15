import numpy as np
from qy.hardware.heaters import dac, calibration_table
from qy.hardware.fpga import fpga
from qy.simulation import linear_optics as lo
from time import sleep
from numpy import pi
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
    experiment_filename='data/%d_experiment.npy' % (heater_index,)
    theory_filename='data/%d_theory.npy' % (heater_index,)
    param_filename='data/%d_parameters.npy' % (heater_index,)
    return experiment_filename, theory_filename, param_filename

def do_measurement(phases, ontime=2, offtime=12):
    voltages=table.get_voltages(phases)
    dac.write_voltages(voltages)
    print 'warming up...'
    for j in range(ontime): 
        fpga.read()
    counts=fpga.read()
    dac.zero()
    print 'cooling'
    for j in range(offtime): 
        fpga.read()
    
    # Get c00, c01, c10, c11
    coincidences=np.array(counts[8:12])
    accidentals=np.array([counts[12], counts[17], counts[16], counts[13]]) 
    corrected_counts=coincidences-accidentals
    probabilities_expt=corrected_counts/float(np.sum(corrected_counts))
    return probabilities_expt
    
device=lo.beamsplitter_network(json='cnot_mz.json')
simulator=lo.simulator(device, nphotons=2)
simulator.set_input_state([1,3])
simulator.set_visibility(0.95)
    
def do_theory(phases, total_counts):
    device.set_phases(phases)
    c00=simulator.get_probability_quantum([1,3])
    c01=simulator.get_probability_quantum([1,4])
    c10=simulator.get_probability_quantum([2,3])
    c11=simulator.get_probability_quantum([2,4])
    counts=np.array([c00, c01, c10, c11])*total_counts
    counts=np.floor(counts)
    counts=np.random.poisson(counts)
    probabilities=counts/float(np.sum(counts))
    return probabilities

def plot_curve(parameter_space, data, style):
    plt.plot(parameter_space, data, style)
    plt.grid(linestyle='-', color='gray')
    #plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$'])
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2], ['0', '$\pi/2$', '$\pi$', '$3\pi/2$', '$2\pi$', '$5\pi/2$'])
    plt.xlim(0, pi*3)
    plt.ylim(0,1)
    
def plot_now(experiment, theory, parameter_space, do_fit):
    labels=['00', '01', '10', '11']
    for column in [0,1,2,3]:
        plt.subplot(221+column)
        plt.text(0.05, 0.95, labels[column], transform=plt.gca().transAxes, va='top')
           
        # Generate theory manifold and plot
        plot_curve(parameter_space, theory[:, column], 'bx')
        plot_curve(parameter_space, experiment[:, column], 'k.')
        
        if do_fit:
            guess=[pi,1,0]
            fitted_params=fit_to_data(experiment[:, column], parameter_space, guess=guess)
            fit_space=np.linspace(0, 3*pi, 300)
            fit=fit_func(fitted_params, fit_space)
            plot_curve(fit_space, fit, 'r-')
        
    plt.savefig('1d_sweep.pdf')
    plt.close()

    
############ DATA ACQUISITION
def acquire_data(heater_index, N=20, hold=[]):
    min_phase, max_phase=0, 3*np.pi
    parameter_space=np.linspace(min_phase, max_phase, N)
    experiment=np.zeros([N, 4])
    theory=np.zeros([N, 4])
    
    for index_1, parameter_1 in enumerate(parameter_space):
        print index_1
        
        # Figure out the settings
        phases=np.zeros(8)
        phases[heater_index]= parameter_1
        for index,phase in hold:
            phases[index]=phase
            
        # Do the measurement
        experiment[index_1] = do_experiment(phases)
        theory[index_1] = do_theory(phases, np.sum(experiment[index_1]))
        
        # Plot
        plot_now(experiment, theory, parameter_space, do_fit=False)

    # Close hardware
    dac.zero()
    
    # Normalize, save and return data
    #data=data/np.amax(data)
    experiment_filename, theory_filename, param_filename = get_filenames(heater_index)
    np.save(experiment_filename, experiment)
    np.save(theory_filename, theory)
    np.save(param_filename, parameter_space)
    return experiment_filename, theory_filename, param_filename

    
dac=dac.dac()
fpga=fpga()
table=calibration_table()

heater_index = 0
#hold_table=[[0,pi/2],[2,0], [6,pi/2]]
hold_table=[[1,pi]]

# Take data
acquire_data(heater_index, hold=hold_table, N=30)

# Reload and fit
#experiment_filename, theory_filename, param_filename = get_filenames(heater_index)
#experiment=np.load(experiment_filename)
#theory=np.load(theory_filename)
#parameter_space=np.load(param_filename)