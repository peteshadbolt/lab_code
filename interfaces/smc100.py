import time, sys
from qy.hardware import smc100
from qy.gui.smc100 import gui
from qy.formats import ctx


if __name__=='__main__':

    def check_gui():
        ''' Check the state of the gui '''
        for key, value in interface.collect():
            if key=='gui_quit':
                motors.kill()
                sys.exit(0)
            


    def smc100_callback(message):
        ''' Handles messages from the SMC100 '''
        key, value = message
        if key=='status':
            interface.send(key, value)



    # The GUI
    interface=gui()

    # The motor controllers
    motors=smc100(callback=smc100_callback)

    print str(motors)
    motors.actuators[3].home()
    motors.actuators[3].move(20)


    # The motor controllers
    while True:
        check_gui()

    motors.kill()

