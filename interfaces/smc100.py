import time, sys
from qy.hardware import smc100
from qy.gui.smc100 import gui
from qy.formats import ctx


if __name__=='__main__':

    #def check_gui():
        #''' Check the state of the gui '''
        #for key, value in interface.collect():
            #print key, value


    #def dpc_callback(message):
        #''' Handles messages from the DPC230 '''
        #interface.send('status', message)

    # The motor controllers
    motors=smc100()
    print str(motors)

    # The GUI
    #interface=gui()

    # The motor controllers

    #while True:
        #counter.count({})
        #check_gui()

    motors.kill()

