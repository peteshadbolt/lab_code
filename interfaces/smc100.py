import time, sys
from qy.hardware import smc100
from qy.gui.smc100 import gui
from qy.formats import ctx


if __name__=='__main__':

    #def check_gui():
        #''' Check the state of the gui '''
        #for key, value in interface.collect():
            #print key, value


    def smc100_callback(message):
        ''' Handles messages from the SMC100 '''
        print message
        #interface.send('status', message)

    # The motor controllers
    smc100=smc100(callback=smc100_callback)
    print str(smc100)
    smc100.actuators[3].home()
    smc100.actuators[3].move(20)


    # The GUI
    #interface=gui()

    # The motor controllers

    #while True:
        #counter.count({})
        #check_gui()

    smc100.kill()

