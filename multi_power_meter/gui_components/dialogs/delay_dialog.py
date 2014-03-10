from Tkinter import *
import tkFileDialog as tkFD

class delay_dialog:
	''' a simple editor for the delays '''
	def __init__(self, parent, delay_file_path):
		''' constructor. we are given the current delay file path '''
		self.tk_root=Toplevel(parent)
		self.tk_root.title('Delay Editor')
		self.tk_root.resizable(0,0)
		self.tk_root.wm_iconbitmap('icon.ico')
		self.build()
		self.delay_file_path=delay_file_path
		self.load_delays()
		self.update()
		
	def shift(self, index, value):
		''' shift a given delay line '''
		v=self.delay_vars[index].get()
		if v>0: self.delay_vars[index].set(v+value)
		
	def get_shifter(self, index, value):
		''' get a lambda to shift a particular delay '''
		return lambda: self.shift(index, value)
		
	def build(self):
		''' build all of the GUI elements '''
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		self.delay_vars=[IntVar() for i in range(16)]
		self.delay_labels=[StringVar() for i in range(16)]
		for i in range(16):
			f=Frame(q); f.pack()
			l=Label(f, textvar=self.delay_labels[i], width=20);	l.pack(side=LEFT, padx=1)
			
			b=Button(f, text=' - ', command=self.get_shifter(i, -1))
			b.pack(side=LEFT)
			
			w = Scale(f, from_=0, to=300, orient=HORIZONTAL, showvalue=0, sliderlength=20, variable=self.delay_vars[i], length=300, width=24)
			self.delay_vars[i].trace('w', self.update)
			w.pack(side=LEFT)
			
			b=Button(f, text=' + ', command=self.get_shifter(i, 1))
			b.pack(side=LEFT)
		
	def update(self, a=0,b=0,c=0):
		alphabet='ABCDEFGHIJKLMNOP'
		for i in range(16):
			tb=self.delay_vars[i].get()
			self.delays[i]=tb
			ns=tb*0.082305
			s='%s = %d tb (%.2f ns)' % (alphabet[i], tb, ns)
			self.delay_labels[i].set(s)
		self.send_delays()
			
	def load_delays(self):
		''' loads delays from a file '''
		self.delays=[0]*16
		try:
			f=open(self.delay_file_path)
			i=0
			for line in f:
				self.delay_vars[i].set(line.strip())
				self.delays[i]=int(line.strip())
				i+=1
			f.close()
		except:
			print 'Error loading delay file %s' % self.delay_file_path
		
	def save_delays(self):
		''' save delays to a file '''
		try:
			s='\n'.join([str(int(v.get())) for v in self.delay_vars])
			f=open(self.delay_file_path, 'w')
			f.write(s)
			f.close()
		except:
			print 'Error saving delay file %s' % self.delay_file_path
