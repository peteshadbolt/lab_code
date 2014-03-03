import wx
import wxbasics
import qy

class motor_block(wx.Panel):
	def __init__(self, parent, index):
		''' a chunk of motor controller stuff '''
		self.index=index
		
		wx.Panel.__init__(self, parent)
		sizer=wx.BoxSizer(wx.HORIZONTAL)
			
		self.input_output=wxbasics.input_output_pair(self, border=True)
		self.input_output.configure(format=float, limits=(0,360))
		self.button=wx.Button(self, label='Go!', size=(40,20))
		sizer.Add(self.input_output, 1, wx.RIGHT, 2)
		sizer.Add(self.button, 0, wx.EXPAND)
			
		self.SetSizerAndFit(sizer)
		self.Fit()
		
	def send_position(self, event=None):
		message={'move_mc':None, 'mc_index': self.index+1, 'position': self.input_output.get_value()}
		self.button_function(message)
		
	def bind_button(self, function):
		self.button_function=function
		self.button.Bind(wx.EVT_BUTTON, self.send_position)
		
class motors_panel(wx.Panel):
	def __init__(self, *args, **kwargs):
		''' panel to control and monitor the motor controllers '''
		wx.Panel.__init__(self, *args, **kwargs)
		mainsizer=wx.BoxSizer(wx.VERTICAL)
						
		self.blocks=[]
		self.need_values=True
		
		for i in range(int(qy.settings.get('motors_count'))):
			block=motor_block(self, i)
			self.blocks.append(block)
			mainsizer.Add(block, 0, wx.TOP|wx.EXPAND, border=2)
		
		self.SetSizerAndFit(mainsizer)
		
	def bind_button(self, function):
		for b in self.blocks:
			b.bind_button(function)
		
	def update(self, state):
		''' got an update from the hardware '''
		for i in range(state.mc_count):
			s='MC%d: %.3f (%s)' % (i+1, state.positions[i], state.states[i])
			self.blocks[i].input_output.set_label(s)
			if self.need_values:
				self.blocks[i].input_output.entry.text.ChangeValue(str(state.positions[i]))
			
		self.need_values=False
