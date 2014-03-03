import winsound

class sounder:
	def __init__(self):
		self.min_f=800
		self.max_f=10000
		self.center=(self.max_f+self.min_f)/2.
		self.set_scaling_factor(10000)
		
	def set_scaling_factor(self, rate):
		if rate==0: return
		self.scaling_factor=self.center/rate
		
	def beep(self, data):
		rate=data[2]
		
		f=int(self.scaling_factor*rate)
		if f>self.max_f or f<self.min_f: 
			self.set_scaling_factor(rate)
		else:
			winsound.Beep(int(f), 100)
		