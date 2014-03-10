import serial
from msvcrt import kbhit
from msvcrt import getch
import datetime

class fpga:
	delays=[0]*8
	finedelays=[0]*8
	modes=[0]*14
	# Constructor
	def __init__(self, COM=0):
		self.serial=serial.Serial()
		self.serial.port=COM
		self.serial.timeout=10
		self.serial.baudrate=9600
		self.serial.bytesize=serial.EIGHTBITS
		self.serial.parity=serial.PARITY_NONE
		self.serial.stopbits=serial.STOPBITS_ONE
		self.initialize()
		
	def initialize(self):	
		print 'initializing FPGA...'
		self.openSerial()
		for i in range(14):
			self.setMode(i,1)
		for i in range(8):
			self.setDelay(i,20,0)
		self.writeDelays()

	def setMode(self,combination=0,mode=0):
		if combination>=0 and combination<=13: self.modes[13-combination]=mode
		
	def setDelay(self,channel=0,delay=0,finedelay=0):
		if delay>75: delay=75
		if finedelay>63: finedelay=63
		if channel>=0 and channel<=7:
			self.delays[7-channel]=delay//5
			self.finedelays[7-channel]=finedelay
			
	def writeDelays(self):
		if self.serial.isOpen():
			# Output the last 2 pairs
			value=self.modes[0]<<2
			value|=self.modes[1]
			
			# Output the modes for the combinations in blocks of 4 pairs of bits
			for i in xrange(2,14,4):
					value=self.modes[i]<<6
					value|=self.modes[i+1]<<4
					value|=self.modes[i+2]<<2
					value|=self.modes[i+3]
					self.serial.write(chr(value))
			self.serial.write(chr(value))

			# Output the delays for each channel
			for delay in self.delays:
				self.serial.write(chr(delay))

			# Output the fine delays for each channel
			for finedelay in self.finedelays:
					self.serial.write(chr(finedelay))
			self.serial.write(chr(250))
			self.serial.write(chr(198))
			self.serial.write(chr(136))
			
	def read(self,op=0):
		self.serial.flush()
		counts=[0]*22
		if self.serial.isOpen():
			charFromSerial=self.serial.read(1)
			if len(charFromSerial)==0:
				print "You might want to try plugging the serial cable in"
				return [0]*22
			zeroword=ord(charFromSerial)
			zeroword2=255
			
			while ((zeroword+zeroword2)!=0):
				zeroword2=zeroword
				zeroword=ord(self.serial.read(1))
		
			# Read the count rates of the 8 channels and the 14 combinations
			for i in xrange(22):
				counts[i]=0
				for j in xrange(0,32,8):
					# Read and store the counts
					word=ord(self.serial.read(1))
					word<<=j
					
					counts[i]|=word
					# Read the 'address' (and ignore it)
					address=ord(self.serial.read(1))
		if counts[21]>100000:
			self.serial.read(2)
			return [0]*22
		return counts
	
	def openSerial(self):
		if not self.serial.isOpen(): self.serial.open()

	def closeSerial(self):
		if self.serial.isOpen(): self.serial.close()
		
	def kill(self):
		print 'closing fpga...'
		self.closeSerial()