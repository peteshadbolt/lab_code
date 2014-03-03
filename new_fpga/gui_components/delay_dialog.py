import wx
import qy
import qy.settings
import wxbasics

class delay_line(wx.Panel):
	def __init__(self, parent, index=0):
		self.index=index
		self.letter=qy.hardware.counting.defs.alphabet_upper[self.index]
		wx.Panel.__init__(self, parent)
		sizer=wx.BoxSizer(wx.HORIZONTAL)
		
		self.slider=wx.Slider(self, value=0, minValue=0, maxValue=200, size=(200,20))
		self.slider.SetLineSize(1)
		sizer.Add(self.slider, 1, wx.EXPAND)
		self.slider.Bind(wx.EVT_SCROLL, self.update)
		
		self.indicator=wx.StaticText(self, label='')
		self.indicator.SetMinSize((130, 20))
		sizer.Add(self.indicator, 0, wx.LEFT, 10)
		self.update()
		self.SetSizerAndFit(sizer)
		
	def set_value(self, n):
		self.slider.SetValue(n)
		self.update()
	
	def get_value(self):
		return self.slider.GetValue()
		
	def update(self, event=None):
		tb=int(self.slider.GetValue())
		ns=tb*0.082305
		s='%s = %d tb (%.2f ns)' % (self.letter, tb, ns)
		self.indicator.SetLabel(s)
		self.indicator.Fit()

class delay_dialog(wx.Dialog):
	def __init__(self, parent, postprocessing_pipe):
		''' a dialog to control the delays '''
		self.delay_file_path=qy.settings.lookup('delay_file')
		self.postprocessing_pipe=postprocessing_pipe
		self.build(parent)		
		self.load_delays()
		
	def build(self, parent):
		wx.Dialog.__init__(self, parent, title='Delay Editor (Use arrow keys for fine control)', size=(350,300))
		self.mainsizer=wx.BoxSizer(wx.VERTICAL)
		self.delay_lines=[]
		for i in range(16):
			d=delay_line(self, i)
			self.delay_lines.append(d)
			self.mainsizer.Add(d, 0, wx.EXPAND|wx.ALL, 10)
		self.SetSizerAndFit(self.mainsizer)
		self.build_timer()
	
	def build_timer(self):
		''' the main loop '''
		self.timer=wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.ontimer, self.timer)
		self.timer.Start(1000)
		
	def ontimer(self, event):
		''' every timer event, send the delays '''
		self.send_delays()

	def send_delays(self):
		''' sends new delay values to the postprocessing server '''
		delays=[q.get_value() for q in self.delay_lines]
		self.postprocessing_pipe.send({'delays':delays})
		
	def load_delays(self):
		''' loads delays from a file '''
		try:
			f=open(self.delay_file_path, 'r')
			i=0
			for line in f:
				self.delay_lines[i].set_value(int(line.strip()))
				i+=1
			f.close()
		except IOError:
			print 'Error loading delay file %s' % sefl.delay_file_path
		
