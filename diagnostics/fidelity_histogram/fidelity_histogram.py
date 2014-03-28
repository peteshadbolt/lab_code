from qy.hardware.heaters import dac, calibration_table
from qy.hardware.fpga import fpga
import numpy as np
from numpy import pi
import time
import datetime
from qy.simulation import linear_optics as lo
from matplotlib.backends.backend_agg import FigureCanvasAgg
from msvcrt import kbhit, getch
from matplotlib.figure import Figure
from qy.analysis.metrics import fidelity as statistical_fidelity

def timestamp(): return datetime.datetime.now().strftime('%a%d%b%Y_%H%M%p').lower()

def get_bin(x):    return int(np.floor(x/bin_size))

def do_measurement(phases, ontime=1, offtime=12):
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
    return counts
    
def new_sample(device):
    #phases=[0,pi,0,0,0,0,0,0]
    #phases=[pi,pi,0,0,0,0,0,0]
    phases=np.random.uniform(0,np.pi*2,8)
    phases[6]=0.93361981
    phases[0]=np.pi
    counts=do_measurement(phases, ontime=2)
    
    coincidences=np.array(counts[8:12])
    accidentals=np.array([counts[12], counts[17], counts[16], counts[13]])
    corrected_counts=coincidences-accidentals
    probabilities_expt=corrected_counts/float(np.sum(corrected_counts))
    print probabilities_expt
    
    '''get some simulated probabilities'''
    device.set_phases(phases)
    simulator=lo.simulator(device, nphotons=2)
    simulator.set_input_state([1,3])
    probabilities_theory=simulator.get_probabilities(patterns=[[1,3],[1,4],[2,3],[2,4]])
    sum_probs=sum(probabilities_theory)
    probabilities_theory=np.array(probabilities_theory)/sum_probs
    fidelity=statistical_fidelity(probabilities_expt, probabilities_theory)
    return np.sum(coincidences), np.sum(accidentals), np.sum(fidelity), phases, coincidences, accidentals
    
def draw_graph():
    fig=Figure()
    
    # histogram
    ax=fig.add_subplot(211)
    hist_x=np.arange(0, 1, bin_size)
    ax.bar(hist_x, fidelity_bins, width=bin_size, facecolor='#6666ff')
    ax.set_xlabel('Fidelity')
    ax.set_ylabel('Frequency')
    ax.set_xlim(minf*0.95, maxf)
    label='Mean Fidelity=%.4f' % fidelity_mean
    ax.text(0.025, 0.95, label, transform=ax.transAxes, fontsize=10, va='top')
    label='Worst Fidelity=%.4f' % minf
    ax.text(0.025, 0.85, label, transform=ax.transAxes, fontsize=10, va='top')
    
    # trace
    ax=fig.add_subplot(212)
    
    N=len(data_coincidences)
    if N>2:
        t=range(N)
        (ar,br)=np.polyfit(t,data_coincidences,1)
        xr=np.polyval([ar,br],t)
        ax.plot(xr, '--', color='#aaaaaa')
    
    ax.plot(data_coincidences, 'b.')
    ax.plot(data_coincidences, 'b-')
    ax.plot(data_accidentals, 'r.')
    ax.plot(data_accidentals, 'r-')
    ax.set_ylabel('Coincidences')
    ax.set_xlabel('Time')
    
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure('output/%s.pdf' % start_time, dpi=100)
    
class fake_fpga:
    def __init__(self):
        self.labels=['AB', 'AD', 'BC', 'CD']
             
    def read(self):
        time.sleep(1)
        return [0]*4
    
fpga=fpga()
table=calibration_table()
dac=dac.dac()
device=lo.beamsplitter_network(json='cnot_mz.json')
simulator=lo.simulator(device, nphotons=2)
simulator.set_input_state([1,3])

start_time=timestamp()
print 'press Q to stop!'

bin_count=400
minf, maxf=1.0,1.0
bin_size=1/float(bin_count)
data_coincidences=[]
data_accidentals=[]
data_phases=[]
data_raw_coinc=[]
data_raw_accid=[]
fidelity_bins=[0]*bin_count
fidelity_samples=0
fidelity_sum=0
fidelity_mean=0

stop=False
while not stop:
    coincidences, accidentals, fidelity, phases, raw_coinc, raw_accid = new_sample(device)
    data_coincidences.append(coincidences)
    data_accidentals.append(accidentals)
    data_phases.append(phases)
    
    print fidelity

    data_raw_coinc.append(raw_coinc)
    data_raw_accid.append(raw_accid)
    fidelity_bins[get_bin(fidelity)]+=1
    minf=min(fidelity, minf)
    maxf=max(fidelity, maxf)
    fidelity_sum+=fidelity
    fidelity_samples+=1.0
    fidelity_mean=fidelity_sum/fidelity_samples
    
    draw_graph()
    if kbhit(): stop = getch()=='q'
    
dac.zero()
