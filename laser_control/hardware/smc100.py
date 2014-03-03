import serial
import time

# here are some constants pertaining to the SMC100
controller_state_map=\
	{'0A': 'NOT REFERENCED from reset',
	'0B': 'NOT REFERENCED from HOMING',
	'0C': 'NOT REFERENCED from CONFIGURATION',
	'0D': 'NOT REFERENCED from DISABLE',
	'0E': 'NOT REFERENCED from READY',
	'0F': 'NOT REFERENCED from MOVING',
	'10': 'NOT REFERENCED ESP stage error',
	'11': 'NOT REFERENCED from JOGGING',
	'14': 'CONFIGURATION',
	'1E': 'HOMING commanded from RS-232-C',
	'1F': 'HOMING commanded by SMC-RC',
	'28': 'MOVING',
	'32': 'READY from HOMING',
	'33': 'READY from MOVING',
	'34': 'READY from DISABLE',
	'35': 'READY from JOGGING',
	'3C': 'DISABLE from READY',
	'3D': 'DISABLE from MOVING',
	'3E': 'DISABLE from JOGGING',
	'46': 'JOGGING from READY',
	'47': 'JOGGING from DISABLE'}
	
# more constants
error_names=\
	['Not used',
	'Not used',
	'Not used',
	'Not used',
	'Not used',
	'Not used',
	'80W output power exceeded',
	'DC voltage too low',
	'Wrong ESP stage',
	'Homing time out',
	'Following error',
	'Short circuit detection',
	'RMS current limit',
	'Peak current limit',
	'Positive end of run',
	'Negative end of run']

class smc100:
	def __init__(self, COM=1):	
		print 'connecting to SMC100...',
		self.serial=serial.Serial()
		self.serial.port=COM
		self.serial.timeout=10
		self.serial.baudrate=57600
		self.serial.bytesize=serial.EIGHTBITS
		self.serial.parity=serial.PARITY_NONE
		self.serial.stopbits=serial.STOPBITS_ONE
		self.serial.open()
		print 'done'
	
	# send a command
	def send(self, command):
		self.serial.write(command+'\r\n')
	
	# send a command and wait for a reply
	def send_rcv(self, command):
		self.serial.write(command+'\r\n')
		return_value=self.serial.readline(100)
		return return_value[len(command):].strip()
		
	# home the controller
	def home(self, controller):
		return self.send('%02dOR' % (controller))
				
	# move to an absolute position
	def move_absolute(self, controller, position):
		return self.send('%02dPA%f' % (controller, position))
		
	# move to an absolute position and wait until the motor catches up
	def move_and_wait(self, controller, position):
		print 'moving controller to %.3f ...' % position
		self.move_absolute(controller, position)
		state=self.get_state(controller)
		while state!="READY from MOVING":
			state=self.get_state(controller)
		print 'done.'
		
	# stop motion
	def stop_motion(self, controller):
		return self.send('%02dST' % (controller))
		
	# move to a relative position
	def move_relative(self, controller, position):
		return self.send_rcv('%02dPR%f' % (controller, position))
		
	# get the current postion of the controller
	def get_position(self, controller):
		return float(self.send_rcv('%02dTP' % (controller)))
	
	# get the state of the controller e.g. "READY from MOVING"
	def get_state(self, controller):
		s=self.send_rcv('%02dTS' % (controller))
		controller_state=controller_state_map[s[-2:]]
		return controller_state
		
	# get a list of errors
	def get_errors(self, controller):
		s = self.send_rcv('%02dTS' % (controller))
		errorstring = ''.join(['%04d' % int(bin(int(c,16))[2:]) for c in s[:-2]])
		return [error_names[i] for i in range(16) if errorstring[i]=='1']
	
	# close the serial connection
	def kill(self):
		self.serial.close()
		print 'disconnected from SMC100'