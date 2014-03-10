import wx
import qy
import wxbasics

class browser_input(wx.Panel):
	def __init__(self, parent):
		''' a label box with an optional border '''
		wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
		self.SetBackgroundColour(wx.Colour(255,255,255))
		
		sizer=wx.BoxSizer(wx.VERTICAL)
		self.text=wx.TextCtrl(self, style=wx.NO_BORDER)
		self.text.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
		sizer.Add(self.text, 0)
		self.SetSizerAndFit(sizer)
		
	def set_value(self, value):
		self.text.SetValue(value)
		
	def get_value(self):
		return self.text.GetValue().upper()

class browser_output(wx.Panel):
	def __init__(self, parent, colour):
		''' a label box with an optional border '''
		wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
		
		self.SetBackgroundColour(colour)
		self.SetDoubleBuffered(True)
		
		sizer=wx.BoxSizer(wx.VERTICAL)
		self.text=wx.StaticText(self, label='', style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
		
		self.text.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
		self.text.SetLabel('')
		sizer.Add(self.text, 1, wx.RIGHT|wx.EXPAND, 4)
		sizer.SetMinSize((150,20))
		self.SetSizerAndFit(sizer)
		
	def set_value(self, value):
		''' set the value of the label '''
		if value==None:
			self.text.SetLabel('--')
		else:
			self.text.SetLabel(format(value, ',d'))

class browser_block(wx.Panel):
	def __init__(self, parent, colour):
		''' a label box with an optional border '''
		wx.Panel.__init__(self, parent)
		self.colour=wx.Colour(*colour)
		sizer=wx.BoxSizer(wx.HORIZONTAL)
		
		self.input=browser_input(self)
		self.output=browser_output(self, self.colour)
		
		sizer.Add(self.input, 0, wx.RIGHT, 2)
		sizer.Add(self.output, 1, wx.EXPAND)
		self.SetSizerAndFit(sizer)
		self.Fit()
		
	def bind(self, function):
		self.input.text.Bind(wx.EVT_TEXT, function)
		
	def get_value(self):
		return self.input.get_value()
		
	def set_label(self, value):
		self.input.set_value(value)
		
	def set_value(self, value):
		self.output.set_value(value)
		
class browser(wx.Panel):
	def __init__(self, parent, number=16):
		''' constructor '''
		wx.Panel.__init__(self, parent)
		self.build()
		
	def build(self):
		''' build the widget '''
		mainsizer=wx.BoxSizer(wx.VERTICAL)
		self.blocks=[]
		for i in range(16):
			colour=qy.graphics.colors.get_pastel_rgb(i)
			colour=wx.Colour(*colour)
			block=browser_block(self, colour)
			block.bind(self.patterns_changed)
			self.blocks.append(block)
			mainsizer.Add(block, 0, wx.TOP|wx.EXPAND, border=2)
		self.SetSizerAndFit(mainsizer)
		
	def bind_change(self, function):
		''' bind a function to the event when any of the widgets changes '''
		self.on_change=function
		
	def set_patterns(self, patterns):
		''' set all of the patterns '''
		for i in range(min(len(patterns), len(self.blocks))):
			self.blocks[i].set_label(patterns[i])
		
	def get_text_patterns(self):	
		''' get all of the patterns as text '''
		return [b.get_value() for b in self.blocks]
		
	def patterns_changed(self, event):
		''' this happens every time the user changes the pattern selection '''
		l=self.get_text_patterns()
		parsed_patterns=qy.hardware.counting.parser.parse_pattern_list(l)
		self.on_change(parsed_patterns)
		
	def update_counts(self, counts):
		''' the postprocessing system sent us new count rates. process them, and forward the filtered counts onto the graph '''
		
		text_patterns=self.get_text_patterns()
		parsed_patterns = qy.hardware.counting.parser.parse_pattern_list(text_patterns, False)
		data=[]
		
		for i in range(len(parsed_patterns)):
			if parsed_patterns[i] in counts:
				self.blocks[i].set_value(counts[parsed_patterns[i]])
				data.append((i, text_patterns[i], counts[parsed_patterns[i]]))
			else:	
				# the requested pattern does not appear in the block sent back by the postprocessor
				if parsed_patterns[i]!=None:
					self.blocks[i].set_value(0)
					data.append((i, text_patterns[i], 0))
				else:
					self.blocks[i].set_value(None)
					
		return data
		
		