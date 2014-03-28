from qy.simulation import qi
from numpy import *

def do(phi1, phi2):
    state=qi.one
    state=qi.dc*state
    state=qi.phase(phi1)*state
    state=qi.dc*state
    state=qi.phase(phi2)*state
    state=qi.dc*state
    print float(abs(state[0]))**2

for phase in linspace(0, 2*pi, 20):
    do(pi/2, phase)

