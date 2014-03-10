from qython.hardware.smc100 import smc100

print 'SMC100 Motor Controller\n'
print 'Commands:'
print 'mv [x]\t\t: Move to position x'
print 'home\t\t: Home'
print 'tell \t\t: Tell current position and status'
print 'quit\t\t: Close COM port, quit program'
print

motors=smc100(COM=7)
print

command=''
while command != 'quit':
	command=raw_input('> ').strip().lower()
	if command.startswith('mv '):
		x=float(command.split(' ')[1])
		motors.move_and_wait(1, x)
		
	if command.startswith('home'):
		motors.home(1)
		
	elif command.startswith('tell'):
		print 'State: %s' % motors.get_state(1)
		print 'Position: %.5f' % motors.get_position(1)
		print 'Errors:', motors.get_errors(1)	
		print

motors.kill()