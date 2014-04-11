import wx
import qy
import matplotlib
matplotlib.rc('font', family='arial', size=8)
matplotlib.interactive(False)
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

import numpy as np

class curve:
	def __init__(self, index, history_size=50):
		self.index=index
		self.colour=qy.graphics.colors.get_color(index)
		self.data=[]
		self.history_size=history_size
		
	def add_point(self, value):
		self.data.append(value)
		if len(self.data)>self.history_size:
			self.data=self.data[1:]
		
	def draw(self, axis, hi_contrast=False):
		col='#ffffff' if hi_contrast else self.colour
		width=3 if hi_contrast else 1
		axis.plot(self.data, color=col, lw=width, linestyle='-', marker='.', markersize=7)

class graph_panel(wx.Panel):
	def __init__(self, *args, **kwargs):
		wx.Panel.__init__(self, *args, **kwargs)
		self.previous_patterns=[]
		self.history_size=100
		self.hi_contrast=False
		self.build()
		
	def build(self):
		self.fig = Figure(dpi=110)
		#self.fig.set_facecolor('#d4d0c8')
		self.fig.set_facecolor('#888888')
		self.canvas = FigCanvas(self, -1, self.fig)
		self.Bind(wx.EVT_SIZE, self.sizeHandler)
		self.SetMinSize((400,200))
		self.clear()
		self.draw()
		
	def sizeHandler(self, *args, **kwargs):
		''' makes sure that the canvas is properly resized '''
		self.canvas.SetSize(self.GetSize())
		
	########################
	
	def set_hi_contrast(self, event):
		''' set the contrast '''
		self.hi_contrast=event.IsChecked()

	def clear(self):
		''' called when the pattern changes '''
		self.need_data=True
		self.singles_curves=[]
		self.coincidence_curves=[]
		
	def add_counts(self, data):
		''' add a set of counts '''
		new_singles=filter(lambda x: len(x[1])==1, data)
		new_coincidences=filter(lambda x: len(x[1])>1, data)
		
		if self.need_data:
			self.singles_curves=[curve(q[0], self.history_size) for q in new_singles]
			self.coincidence_curves=[curve(q[0], self.history_size) for q in new_coincidences]
			self.need_data=False
			
		for i in range(len(self.singles_curves)):
			self.singles_curves[i].add_point(new_singles[i][2])
			
		for i in range(len(self.coincidence_curves)):
			self.coincidence_curves[i].add_point(new_coincidences[i][2])
		self.draw()
		
	def draw_curve_set(self, curves, subplot_index):
		ax=self.fig.add_subplot(subplot_index)
		ax.set_axis_bgcolor('#000000')
		for c in curves:
			c.draw(ax, self.hi_contrast)
		ax.set_xlim(0, self.history_size)
		yfm=ax.yaxis.get_major_formatter()
		yfm.set_powerlimits([0,1])
		
	def draw(self):
		''' draw all of the curves etc '''
		self.fig.clf()
		self.draw_curve_set(self.singles_curves, 211)
		self.draw_curve_set(self.coincidence_curves, 212)
		self.fig.subplots_adjust(left=.05, right=.98, top=.97, bottom=.05)
		self.canvas.draw()