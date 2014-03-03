# program to manually control the laser
from qy.hardware import toptica
import time

print 'TOPTICA iBEAM\n'
print 'Commands:'
print 'la on\t\t: Switch laser on'
print 'la off\t\t: Switch laser off'
print 'set pow [x]\t: Set power to [x] mW'
print 'quit\t\t: Close COM port, quit program'
print
# make COM port connection
laser=toptica(COM=6)
print

command=''
while command != 'quit':
	command=raw_input('> ').strip().lower()
	laser.send(command)
	
laser.kill()
time.sleep(3)
