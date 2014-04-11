import time, sys
from qy.hardware import smc100
from qy.gui.smc100 import gui
from qy.formats import ctx


if __name__=='__main__':

    def check_gui():
        ''' Handles messages from the GUI '''
        for key, value in interface.collect():
            if key=='move':
                address=value['controller_address']
                position=value['position']
                motor_controller.actuators[address].move(position)
            elif key=='gui_quit':
                motor_controller.kill()
                sys.exit(0)


    # Make the GUI
    interface=gui()

    # Boot up the motor controllers
    motor_controller=smc100(callback=lambda x: interface.send(x[0], x[1]))

    # Populate the GUI according to the current motor controller situation
    interface.send('populate', motor_controller.dict())

    # Loop forever
    while True:
        check_gui()
        time.sleep(.1)


